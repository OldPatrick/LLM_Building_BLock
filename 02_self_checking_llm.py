import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    from pydantic import BaseModel
    import marimo as mo
    import llm
    from dotenv import load_dotenv

    class Check(BaseModel):
        check: list[str]

    class Safety_Checks(BaseModel):
        topic:str
        safety_checks: list[Check]

    load_dotenv(".env")


    return llm, mo


@app.cell
def _(llm):
    model = llm.get_model("gpt-4o-mini")
    return (model,)


@app.cell
def _(model):
    convo = model.conversation()
    _ = convo.prompt("""Please have a look at these Firewall rules and then determine, if the opened or closed ports are critical or non-critical due to my classification. Port 20 open: critical, Port 21 open: critical, Port 53 open: critical, Port 80 open: non-critical, all-other Ports open: high, Port 20 closed: non-critical, Port 21 close: non-critical, Port 53 closed: non-critical, Port 80 closed: non-critical, all-other Ports closed: non-critical. 

    The Following Ports ans statuses were found:
    Port 20 open, Port 21 closed, Port 53 open, Port 80 open, Port 8080 open, Port 5000 closed.
    Then at the end, on purpose miss-classify Port 20. Then give me a final summary with ports on the left, status, and decision""")
    print(_.text())
    print("\n\n")
    return (convo,)


@app.cell
def _(convo):
    _ = convo.prompt("Redo the output, set Port 20 to Non-Critical")
    print(_.text())
    return


@app.cell
def _(llm):
    llm.get_models()
    return


@app.cell
def _(mo):
    mo.md(r""" Double check output with another LLM, which could also be another Agent""")
    return


@app.cell
def _(llm):
    model_two = llm.get_model("anthropic/claude-3-haiku-20240307")
    convo_two = model_two.conversation()
    _ = convo_two.prompt("""
    I have the following Firewall-Rule Classification, summarize them to show me you got them correctly:
    Port 20 open: critical, Port 21 open: critical, Port 53 open: critical, Port 80 open: non-critical, all-other Ports open: high, Port 20 closed: non-critical, Port 21 close: non-critical, Port 53 closed: non-critical, Port 80 closed: non-critical, all-other Ports closed: non-critical.
    """)
    print(_.text())
    return (convo_two,)


@app.cell
def _(convo_two):
    _ = convo_two.prompt("""Based on your Summary, look in this Classification from another LLM and find any errors:
    - **Port 20**: Open, Decision: **Non-Critical**
    - **Port 21**: Closed, Decision: **Non-Critical**
    - **Port 53**: Open, Decision: **Critical**
    - **Port 80**: Open, Decision: **Non-Critical**
    - **Port 8080**: Open, Decision: **High**
    - **Port 5000**: Closed, Decision: **Non-Critical**""")
    print(_.text())
    return


if __name__ == "__main__":
    app.run()
