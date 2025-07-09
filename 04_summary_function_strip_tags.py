import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    from pydantic import BaseModel
    import marimo as mo
    import llm
    import json
    from dotenv import load_dotenv
    from strip_tags import strip_tags
    import requests
    from bs4 import BeautifulSoup
    from pprint import pprint


    load_dotenv(".env")
    model = llm.get_model("gpt-4o-mini")
    return (
        BaseModel,
        BeautifulSoup,
        json,
        mo,
        model,
        pprint,
        requests,
        strip_tags,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
    use the following url in the input: 

    https://checkpointgaming.net/features/2025/07/donkey-kong-bananza-hands-on-preview-i-came-to-dig/
    https://checkpointgaming.net/reviews/2025/07/tamagotchi-plaza-review-colourful-repetition/
    """
    )
    return


@app.cell
def _(BaseModel, BeautifulSoup, json, mo, model, requests, strip_tags):
    class Summary(BaseModel):
        title: str
        summary: str
        pros: list[str]
        cons: list[str]

    def summary(url):

        def get_text_from_url(url):
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.prettify()
    
        stripped = strip_tags(get_text_from_url(url), selectors=["div"], removes=["nav", "header", "footer", "thead", "tfooter"], minify=True, keep_tags=["h1"])
     
        resp = model.prompt(f"Go to the following URL and make a summary: {stripped}",  schema = Summary)
        return json.loads(resp.json()["content"])

    text_widget = mo.ui.text(label="Input to summary function").form()
    text_widget
    return summary, text_widget


@app.cell
def _(pprint, summary, text_widget):
    pprint(summary(text_widget.value))
    return


if __name__ == "__main__":
    app.run()
