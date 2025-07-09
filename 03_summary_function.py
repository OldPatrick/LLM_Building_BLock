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
    load_dotenv(".env")
    model = llm.get_model("gpt-4o-mini")
    return BaseModel, json, mo, model


@app.cell
def _(BaseModel, json, mo, model):
    class Summary(BaseModel):
        title: str
        summary: str
        pros: list[str]
        cons: list[str]
    
    def summary(text_in):
        resp = model.prompt(f"Make a summary of the following text: {text_in}",  schema = Summary)
        return json.loads(resp.json()["content"])

    text_widget = mo.ui.text_area(label="Input to summary function").form()
    text_widget
    return summary, text_widget


@app.cell
def _(mo):
    mo.md(
        r"""
    original review:
    #https://checkpointgaming.net/reviews/2025/07/tamagotchi-plaza-review-colourful-repetition/

    the review: I’ve been a big fan of Tamagotchi since I was a kid. I even still have all of my original Tamagotchi’s lying around my house, even though these days most of them are in varying stages of deceased. These digital pets have been having a bit of a comeback with the releases of newer, smaller Tamagotchi models and the announcement of tie-in games like Tamagotchi Plaza.


    The gameplay loop of the traditional digital pet is addictive and very comprehensible, but it is always interesting to see the franchise branch out and find ways to use the Tamagotchi characters in more traditional games that don’t revolve around needing to feed them every five minutes. There is a lot of love out there for the designs of many of the Tamagotchi characters, and it could be great to have a new way to see them walking around in a 3D environment.

    Tamagotchi Plaza begins with Prince Tamahiko arriving to collect the player and transport them to Tamahiko town. When they arrive, the residents are all abuzz with news that the Tamagotchi King will soon be selecting a town to host the Tamagotchi Fest and that Tamahiko Town is in the running. The main goal of the game is to help the local shop owners improve their businesses, earn money to renovate the town and hopefully be chosen as the town to host the festival.

    Each shop in the town houses a minigame relating to the business’s main output. You create manga in the manga store and repair bikes in the bicycle store, and so on. Each of the minigames is incredibly brief, lasting only a few minutes each and doing multiple of the same game in a row makes it clear how repetitive the tasks are. At the galette shop, for instance, you cook various savoury crepes for the Tamagotchi that visit the store, and after doing several in a row I quickly realised that I was only ever getting one or two variations of order, meaning that I just had to make the same two crepes over and over again. More options do open up gradually as the shops expand, but everything is released at a drip-feed, and it takes a long time for there to be any significant variety between customer orders.

    Most of the minigames have as much substance as something that you could find online in intellectual property theft games for toddlers that fill the likes of Girlsgogames these days. While they are visually appealing and the bleepy-bloopy noises that represent the characters’ voices are very cute, the minigames themselves struggle to be engaging in any meaningful way. They are also often very poorly tutorialised, which is surprising given the target age demographic for the game. At the manga shop, for example, you will be asked to create a manga page such as ‘Kuchipatchi’s beach magic’ where you need to select the correct images to meet this criteria. The issue is that you might have no idea which Tamagotchi Kuchipatchi is, and you also might not know which object represents magic within the selection. It results in an odd bit of trial and error.

    Tamagotchi Plaza also suffers from not allowing the use of the Nintendo Switch’s touch screen, instead forcing players to scroll through menus and navigate with a slow-moving cursor while trying to play the games. These sorts of minigames are usually made with either a mouse or touchscreen in mind, as they mostly involve dragging things around the screen that just doesn’t feel as snappy when controlled with a joystick.

    On their own, the issues with the minigames in Tamagotchi Plaza aren’t a huge problem, but unfortunately, the main gameplay loop revolves around grinding these minigames to eventually raise each of the stores to ‘royal’ status. Each of the stores needs to be upgraded, too, meaning there is no leeway for you to only spend time playing through the games that you find most enjoyable. As much time spent on the surprisingly enjoyable rap battle minigame, must also have been spent on the dreaded dentist one.

    Aesthetically, though, Tamagotchi Plaza does have a lot going for it. The Tamagotchi characters transition well to the bright 3D environment, and the vocal bleeps and bloops are incredibly endearing. There are lots of characters to bump into, and it’s almost guaranteed that your favourite virtual pet will make an appearance at some point. The building designs are very cute as well, most of them having faces and clear distinctions to what kind of services are offered inside.

    There is also a small Plaza area outside of the stores that can be explored in between shifts at the various shops. It’s very relaxing to walk around in, and various characters can be encountered while outside. Sometimes they lounge around in the park or line up for shops; there are even very small side quests that the characters will offer while you’re out and about. I do wish the world felt a little more reactive, though, while there are upgrades to make to the plaza, the first few are very minimal. The game also lacks a day/night cycle or any sort of weather system, which can leave it feeling very static.
    """
    )
    return


@app.cell
def _(summary, text_widget):
    from pprint import pprint

    pprint(summary(text_widget.value))
    return


if __name__ == "__main__":
    app.run()
