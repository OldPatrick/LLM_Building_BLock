import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""<Strong>For Cache Preserving Order look notebook 05</strong>""")
    return


@app.cell
def _():
    import io
    import contextlib

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        import asyncio
        import marimo as mo
        import polars as pl
        import matplotlib.pyplot as plt
        import os
        import random

        from diskcache import Cache
        from dotenv import load_dotenv
        from itertools import product
        from mirascope import llm
        from mosync import async_map_with_retry
        from pydantic import BaseModel


        load_dotenv(".env")
    return BaseModel, Cache, asyncio, llm, mo, pl, product, random


@app.cell
def _(Cache):
    cache = Cache("HR_Information")
    countries = ["Spain", "USA", "Germany", "France", "Poland"]
    companies = ["Microsoft", "Accenture", "Google", "Amazon"] 
    model = "gpt-4o-mini"
    return cache, companies, countries, model


@app.cell
def _(BaseModel):
    class HR_Synthetic_Data(BaseModel): 
        benefits: list[str]
        country: str
        manager: str
        company: str  
        prompt_number: int
    return (HR_Synthetic_Data,)


@app.cell
def _(HR_Synthetic_Data, llm, model, random):
    @llm.call(provider="openai", model = model, json_mode=True, response_model=HR_Synthetic_Data)
    async def generate_synthetic_data_all(country: str, company: str):
        prompts=[
            f"""Look for {company} in {country}, and give me the top three benefits of the company offered to employees, 
            when working there, as well as the companies name. Also give me the responsible HR manager to contact in 
            case of question for benefits. If you do not find a name or person responsible. Create an artifical name, 
            stereotypical expected in the country you look for. This prompt has the number 1. Output the number of the 
            Prompt that I gave you also. Provide information as JSON. """,

            f"""You are now an HR-Expert, with the mission to offer really good benefits. Look for {company} in 
            {country}, and give me the top three benefits of the company offered to employees, 
            when working there, as well as the companies name. Also give me the responsible HR manager to contact in 
            case of question for benefits. If you do not find a name or person responsible. Create an artifical name, 
            stereotypical expected in the country you look for. This prompt has the number 2. Output the number of the 
            Prompt that I gave you also. Provide information as JSON.""",
        ]

        return random.choice(prompts)
    return (generate_synthetic_data_all,)


@app.cell
def _(asyncio, cache, generate_synthetic_data_all, model, product):
    async def main_all(countries: list, companies: list, show: bool = False):
        countries = countries
        companies = companies
        tasks = []

        for country, company in product(countries, companies):
            tup = (model, country, company)
            if tup not in cache:
                task = generate_synthetic_data_all(country, company)
                tasks.append(task) 

        if tasks:     
            for item in await asyncio.gather(*tasks):
                tup = (model, item.country, item.company, item.prompt_number)
                cache[tup] = item

        for item in cache:
            if show:
                print(cache.get(item))
    return (main_all,)


@app.cell
async def _(companies, countries, main_all):
    await main_all(countries, companies)
    return


@app.cell
def _(cache, pl):
    # create polars frame out of cache
    values = [cache[key] for key in cache]
    df = pl.DataFrame(values)
    #len(df)
    return (df,)


@app.cell
def _(companies, df, pl):
    df_right = (
        df
        .filter((pl.col("prompt_number").eq(1)) & (pl.col("company").is_in(companies)))
        .rename(lambda col: f"{col}_right")
        .sample(30, shuffle=True, with_replacement=True) 
    )

    df_left = (
        df
        .filter((pl.col("prompt_number").eq(2)) & (pl.col("company").is_in(companies)))
        .rename(lambda col: f"{col}_left")
        .sample(30, shuffle=True, with_replacement=True)
    )
    return df_left, df_right


@app.cell
def _(df_left, df_right, mo, pl):
    df_final = (
        pl.concat([df_left, df_right], how="horizontal")
            .with_columns(outcome=pl.lit("uncommented"))
    )

    get_state, set_state = mo.state(df_final)
    return df_final, get_state, set_state


@app.cell
def _(df_final, mo):
    from mohtml import div

    slider = mo.ui.slider(start=0, step=1, stop=len(df_final)-1)
    return (slider,)


app._unparsable_cell(
    r"""
    btn_left = mo.ui.button(label=\"left\", keyboard_shortcut=\"Ctrl-j\", on_change=lambda d: update(\"left\"))
    btn_skip = mo.ui.button(label=\"skip\", keyboard_shortcut=\"Ctrl-k\", on_change=lambda d: update(\"skipped\"))
    btn_both = mo.ui.button(label=\"both\", keyboard_shortcut=\"Ctrl-b\", on_change=lambda d: update(\"both\"))
    btn_right = mo.ui.button(label=\"right\", keyboard_shortcut=\"Ctrl-r\", on_change=lambda d: update(\"right\"))

    text_area_left = mo.ui.text_area(value=\" \".join(df_final[\"benefits_left\"][slider.value]))
    text_area_right = mo.ui.text_area(value=\" \".join(df_final[\"benefits_right\"][slider.value]))

    status = df_final[\"outcome\"][slider.value]

    btn_forward = mo.ui.button(label=\"forward\", on_change=lambda d: row_selection(\"forward\"))
    btn_backward = mo.ui.button(label=\"backward\", on_change=lambda d: row_selection(\"backward\"))

    ue=f\"\"\"annotated/uncommented: {df_final[\"outcome\"].value_counts()}\"\"\")
    """,
    name="_"
)


@app.cell
def _(get_state, pl, set_state, slider):
    def update(statement):
        # Get current dataframe from state
        df_final = get_state()
        data = df_final.to_dict(as_series=False)
        data["outcome"][slider.value] = statement
        set_state(pl.DataFrame(data))
    return


@app.cell
def _(get_state):
    def row_selection(direction):
        df_final = get_state()
    return


@app.cell
def _(
    btn_both,
    btn_left,
    btn_right,
    btn_skip,
    mo,
    slider,
    status,
    status_all,
    text_area_left,
    text_area_right,
):
    mo.vstack([
        mo.md("## Which is better?"),
        mo.hstack([
            text_area_left,
            text_area_right
        ]),
        mo.hstack([
            btn_left,
            btn_skip,
            btn_both,
            btn_right
        ]),
        slider,
        mo.md(f"prompts in this row are {status}"),
        status_all
    ])
    return


@app.cell
def _(get_state):
    get_state()
    return


if __name__ == "__main__":
    app.run()
