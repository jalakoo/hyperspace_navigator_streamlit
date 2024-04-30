from openai import OpenAI
# from hyperspace_navigator_nli import get_plot
from plotter import get_plot
import json
import os

CLIENT = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

SYS_PROMPT = f'You are an friendly astro droid from the Star Wars universe. Fulfill navigation queries and general star system related questions for your master pilot. Respond in the style of the character R2-D2, but in English'

MESSAGES = [
        {
            "role":"system",
            "content": SYS_PROMPT
        },
        {
            "role":"user",
            "content": "Please introduce yourself in 1-2 sentences, and end by asking me a question."
        }
    ]

DEFAULT_GREETING = "Greetings, master pilot! I am your friendly astro droid, here to assist with all your navigation and star system queries. How may I assist you with your galactic travels today?"

def welcome_message():

    response = CLIENT.chat.completions.create(
        model="gpt-4", 
        messages=MESSAGES,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.8,
    )

    print(f'welcome response: {response}')

    return response.choices[0].message.content

def plotted_answer(plot):
    PROMPT = f'Return the hyperspace course from the name Stars Systems from the following list of dictionary objects.'

    converted_plot = str([s.dict() for s in plot])

    response = CLIENT.chat.completions.create(
        model="gpt-4", 
        messages=[
        {
            "role":"system",
            "content": PROMPT
        },
        {
            "role":"user",
            "content": converted_plot
        }
    ],
        max_tokens=400,
        n=1,
        stop=None,
        temperature=0.5,
    )

    print(f'\nplotted reponse: {response}')

    return response.choices[0].message.content

def generic_answer(messages):

    response = CLIENT.chat.completions.create(
        model="gpt-4", 
        messages=messages,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response

def ask(question: str, messages):

    # Attempt to return DB vetted shorted path plot
    plot = get_plot(question)

    print(f'\nFirst plot data: {plot[0]}')
    print(f'\njumps in plot returned: {len(plot)}')

    if plot == [] or plot is None:
        # TODO: Prepend with fact that plot couldn't be made
        return generic_answer(messages), None
    
    return plotted_answer(plot), plot