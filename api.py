from fastapi import FastAPI
from pydantic import BaseModel
import datetime
app = FastAPI()

statecodes = {
    'West Bengal' :'WB',
    'Telangana': 'TG',
    'Maharashtra': 'MH',
    'Karnataka':'KA',
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
    if state == "Goa":
        if data == "Daily Cases":
            sqlquery = f"SELECT date, cases_new FROM {statecode}_overview"
        elif data == "Daily Deaths":
            sqlquery = f"SELECT date, deaths_new FROM {statecode}_overview"
    else:
        sqlquery = f"SELECT date, {datacode} FROM {statecode}_case_info"
            
    return {"sqlquery" : sqlquery, "datatype" :datacode}

class DataClean(BaseModel):
    dirtydata :list
    datatype: str

@app.post("/clean")
def clean(dirtydata:DataClean):
    
    plotdata = dirtydata.dict()
    
    datatype = datacodes[plotdata['datatype']]
    
    plotdata = plotdata["dirtydata"]
    
    for i in range(len(plotdata)):
        if plotdata[i][datatype] == None:
            if i == 0:
                plotdata[0][datatype] = 0
            else:
                plotdata[i][datatype] = plotdata[i-1][datatype]
    
    dates = [datetime.datetime.strptime(ts['date'], "%Y-%m-%d") for ts in plotdata]

    dates.sort()

    sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
    sorteddict = []
    for i in sorteddates:
        for j in range(len(plotdata)):
            if i == plotdata[j]['date']:
                sorteddict.append(plotdata[j])
    
    return {"data" : sorteddict}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)