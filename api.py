from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

statecodes = {
    'West Bengal' :'WB',
    'Telangana': 'TG',
    'Maharashtra': 'MH',
    'Karnataka':'KA',
    'Uttarakhand' : 'UK',
    'Goa':'GA',
    'Delhi':'DL'
}
datacodes = {
    'Daily Cases':'cases_new',
    'Daily Deaths':'deaths_new'
}
class Data(BaseModel): #Type of incoming data
    state: str
    data: str

@app.post("/process")
def process(data: Data):
    
    inputdata = data.dict()
    
    state = inputdata['state']
    data = inputdata['data']
    
    statecode = statecodes[state]
    datacode = datacodes[data] # type: ignore
    sqlquery = None
    if state == "Delhi":
        if data == "Daily Cases":
            sqlquery = f"SELECT date,cases_positive FROM {statecode}_case_info"
        elif data == "Daily Deaths":
            sqlquery = f"SELECT date,deaths FROM {statecode}_case_info"
    elif state == "Goa":
        if data == "Daily Cases":
            sqlquery = f"SELECT date, total_cases_new FROM {statecode}_case_info"
        elif data == "Daily Deaths":
            sqlquery = f"SELECT date, deaths_new FROM {statecode}_case_info"
    else:
        sqlquery = f"SELECT date, {datacode} FROM {statecode}_case_info"
            
    return {"sqlquery" : sqlquery}

class DataClean(BaseModel):
    dirtydata :list

@app.post("/clean")
def clean(dirtydata:DataClean):
    
    plotdata = dirtydata.dict()
    
    plotdata = plotdata["dirtydata"]
    
    for i in range(len(plotdata)):
        if plotdata[i]["cases_new"] == None:
            if i == 0:
                plotdata[0]['cases_new'] = 0
            else:
                plotdata[i]["cases_new"] = plotdata[i-1]["cases_new"]
    
    return {"data" : plotdata}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)