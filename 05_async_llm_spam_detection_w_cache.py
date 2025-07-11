import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
    <Strong>Cache Does Not Preserve Order of Insertion</strong>

    One important thing to understand about the diskcache (and many other cache implementations) is that it is a key-value store, not a data structure that preserves the order of insertion or retrieval. When you iterate over the cache using methods like keys(), iterkeys(), or view().iterkeys(), the order of the keys returned is not necessarily the order in which they were inserted. The cache is essentially a hash-based structure, and the order of keys is typically not guaranteed.
    """
    )
    return


@app.cell
def _():
    import asyncio
    import llm
    import marimo as mo
    import polars as pl
    import matplotlib.pyplot as plt

    from dotenv import load_dotenv
    from datasets import load_dataset
    from mosync import async_map_with_retry
    from diskcache import Cache
    from sklearn.metrics import confusion_matrix, precision_score
    load_dotenv(".env")
    return (
        Cache,
        async_map_with_retry,
        confusion_matrix,
        llm,
        load_dataset,
        mo,
        pl,
        precision_score,
    )


@app.cell
def _(llm):
    # Show Async-Ready Models
    for model in llm.get_async_models():
        print(model.model_id)
    return


@app.cell
def _(load_dataset):
    # Huggingface dataset about spam: 
    # https://huggingface.co/datasets/Deysi/spam-detection-dataset
    df = load_dataset("Deysi/spam-detection-dataset")
    return (df,)


@app.cell
def _(df):
    df_train = df["train"].to_polars()
    df_test = df["test"].to_polars()
    return (df_test,)


@app.cell
def _(Cache, llm):
    cache = Cache("LLM_Prompt_Cache")

    models = {
        "gpt-4": llm.get_async_model("gpt-4"),
        "gpt-4o": llm.get_async_model("gpt-4o"),
        "sonnet2024": llm.get_async_model("anthropic/claude-3-5-sonnet-20241022"),
        "haiku": llm.get_async_model("anthropic/claude-3-haiku-20240307")

    }
    return cache, models


@app.cell
def _():
    prompt = "is this spam or ham? only reply with spam or ham"
    base_llm = "sonnet2024"
    return base_llm, prompt


@app.cell
def _(base_llm, cache, models, prompt):
    async def classify(text, prompt=prompt, model=base_llm):
        tup = (text, prompt, model)
        if tup in cache:
            #check if cached result is found
            print(tup in cache)
            return cache[tup]
        resp = await models[model].prompt(prompt + "\n" + text).json()
        cache[tup] = resp
        return resp
    return (classify,)


@app.cell
async def _(classify):
    await classify("hello there")
    return


@app.cell
async def _(async_map_with_retry, classify, df_test):
    n_eval = 50

    llm_results = await async_map_with_retry(
        [_["text"] for _ in df_test.head(n_eval).to_dicts()], 
        classify, 
        max_concurrency=3, 
        description="Running LLM experiments"
    )

    llm_results_list = []
    print(len(llm_results_list))
    return llm_results, llm_results_list


@app.cell
def _(llm_results, llm_results_list):
    #store the prompt as key, to be sure, that you have a contant match between predictions from cache and real labels
    for k, result in enumerate(llm_results):
        llm_results_list.append((result.item, result.result["content"][0]["text"]))

    print(len(llm_results_list))
    llm_results_list
    return


@app.cell
def _(df_test, llm_results_list, pl):
    df_test_labels = (
        df_test.head(50).with_columns(
            trues = pl.when(pl.col("label").eq("not_spam")).then(pl.lit("ham")).otherwise(pl.lit("spam"))
        ).select("text", "trues")
    )

    llm_frame = pl.DataFrame(llm_results_list, schema=["text", "label_llm"], orient="row")

    df_equal = (
        llm_frame
            .join(df_test_labels, on="text")
            .with_columns(
               trues = pl.when(pl.col("trues").eq("ham")).then(1).otherwise(0),
               label_llm = pl.when(pl.col("label_llm").eq("ham")).then(1).otherwise(0)
            )
    )
    return (df_equal,)


@app.cell
def _(confusion_matrix, df_equal):
    cm = confusion_matrix(y_true=df_equal["trues"], y_pred=df_equal["label_llm"])
    cm
    return


@app.cell
def _(base_llm, df_equal, precision_score, prompt):
    print("model: ", base_llm, "prompt: ", prompt, "Precision:", precision_score(df_equal["trues"], df_equal["label_llm"], average='weighted'), "%")
    return


@app.cell
def _(base_llm, df_equal, precision_score, prompt):
    print("model:", base_llm, "prompt: ", prompt, "Precision:", precision_score(df_equal["trues"], df_equal["label_llm"], average='weighted'), "%")
    return


@app.cell
def _(cache):
    cache.peekitem()
    return


@app.cell
def _():
    #import numpy as np
    #from sklearn.pipeline import make_pipeline
    #from sklearn.linear_model import LogisticRegression
    #from sklearn.feature_extraction.text import CountVectorizer
    #
    #df_valid, df_train = df.head(200), df.tail(200)
    #text_valid = df_valid["text"].to_list()
    #text_train = df_train["text"].to_list()
    #y_valid = df_valid["label"].to_list()
    #y_train = df_train["label"].to_list()
    #
    #pipe = make_pipeline(CountVectorizer(), LogisticRegression())
    #
    ## It's pretty dang accurate
    #preds = pipe.fit(text_train, y_train).predict(text_valid)
    #np.mean(preds == np.array(y_valid))
    return


if __name__ == "__main__":
    app.run()
