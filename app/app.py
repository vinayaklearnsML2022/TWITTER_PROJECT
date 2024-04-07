from fastapi import FastAPI, Query, Path

app = FastAPI()


search = {
1:{
    "name":"hi, please search some option"
  
}
}


@app.get("/search_query/1")
def search_query_1():
    return search[1]


@app.put("/update_query/{query}")
def update_query(query:str):
    search[1]['name']=query
    return search[1]

