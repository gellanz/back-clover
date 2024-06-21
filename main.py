import uvicorn
# To run the application, use the command:
# uvicorn your_script_name:app --reload
if __name__ == "__main__":
    uvicorn.run("app.api:app", host="127.0.0.1", port=8000, reload=True, log_level="info")