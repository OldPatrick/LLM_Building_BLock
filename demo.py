# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import llm
    from dotenv import load_dotenv
    return llm, load_dotenv


@app.cell
def _(load_dotenv):
    load_dotenv(".env")
    return


@app.cell
def _(llm):
    llm.get_models()
    return


@app.cell
def _(llm):
    model_one = llm.get_model("gpt-4o-mini")
    return


@app.cell
def _(llm):
    model_two = llm.get_model("anthropic/claude-3-5-sonnet-20241022")
    return


@app.cell
def _():
    #resp = model_one.prompt("Write a one-liner haiku")
    return


@app.cell
def _():
    #resp2 = model_two.prompt("Write a one-liner haiku")
    return


@app.cell
def _():
    #resp.json(), resp2.json()
    return


app._unparsable_cell(
    r"""
    [
    {
    \"content\":\"Whispers of the breeze, dancing leaves in twilight's glow, night's soft hymn begins.\"
    \"finish_reason\":\"stop\"
    \"usage\":{
    \"completion_tokens\":22
    \"prompt_tokens\":14
    \"total_tokens\":36
    \"completion_tokens_details\":{
    \"accepted_prediction_tokens\":0
    \"audio_tokens\":0
    \"reasoning_tokens\":0
    \"rejected_prediction_tokens\":0
    }
    \"prompt_tokens_details\":{
    \"audio_tokens\":0
    \"cached_tokens\":0
    }
    }
    \"id\":\"chatcmpl-Br0iYFFptXpV1G6NgdTisCitFtIfu\"
    \"object\":\"chat.completion.chunk\"
    \"model\":\"gpt-4o-mini-2024-07-18\"
    \"created\":1751973842
    }
    {
    \"id\":\"msg_01WXmjjKuvBSzBc8iK8f2jJC\"
    \"content\":[
    {
    \"citations\":None
    \"text\":\"leaves dance in wind's breath\"
    \"type\":\"text\"
    }
    ]
    \"model\":\"claude-3-5-sonnet-20241022\"
    \"role\":\"assistant\"
    \"stop_reason\":\"end_turn\"
    \"stop_sequence\":None
    \"type\":\"message\"
    }
    ]
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
