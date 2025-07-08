import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _():
    from pydantic import BaseModel
    import marimo as mo
    import llm
    from dotenv import load_dotenv

    class Haiku(BaseModel):
        poem: list[str]

    class Haikus(BaseModel):
        topic:str
        haikus: list[Haiku]


    return Haikus, llm, load_dotenv


@app.cell
def _(load_dotenv):
    load_dotenv(".env")
    return


@app.cell
def _(Haikus, llm):
    model = llm.get_model("gpt-4o-mini")
    out = model.prompt("Haiku about Python", schema=Haikus)
    return (out,)


@app.cell
def _():
    # Haikus are now a list of Strings:
    import json 
    return (json,)


@app.cell
def _(json, out):
    json.loads(out.json()["content"])
    return


if __name__ == "__main__":
    app.run()
