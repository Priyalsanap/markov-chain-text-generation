import dash
import os
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from collections import Counter
import dash_bootstrap_components as dbc
import json
import random


app = dash.Dash(name='Text_Generation_Using_Markov_Chain', external_stylesheets=[dbc.themes.BOOTSTRAP], serve_locally=False)
app.css.append_css({"external_url": "static/assets/01_markov.css"})

chapters = [file for file in os.listdir(os.path.join(os.getcwd(), 'static/Data/sherlock/'))]

# Define App Layout
app.layout = html.Div([
    html.Div(
        [html.H2('Text Generation Using Markov Chains')], style={'text-align': 'center'}
    ),

    html.Div(className='dropdowns', children=[
        html.Div(id='chapter', children=[
            html.Div(className="btn btn-secondary btn-lg", children=[
                html.H6('Select Chapter to see text')]),
            dcc.Dropdown(id='pick_chapter',
                         options=[{'label': i, 'value': i} for i in chapters], value='')
        ]),

        html.Div(id='Text_Input', children=[
            html.Div(className="btn btn-secondary btn-lg", children=[
                html.H6('Write two words')]),
            dcc.Input(id='choose_words',
                      value='dear holmes '),
        ]),
        # Submit Button
        html.Button('Submit', className="btn btn-primary", id='submit-val', n_clicks=0),
    ]),

    html.Div(className='text_area', children=[
        html.Div(children=[
            dcc.Textarea(
                id='chapter-text',
                value='Text from the selected chapter will appear here.',
                style={'width': '99%', 'height': 600},
            )
        ]),
        html.Div(children=[
            dcc.Textarea(
                id='generated-text',
                value='Text generated using Markov Chain with given input will appear here.',
                style={'width': '99%', 'height': 600},
            )
        ])
    ])

])


# Function to generate text based on a Markov model
def generate_text(markov_model_input, limit=50, start='the adventure '):
    """
    Generate text based on a Markov model.

    Parameters:
    markov_model_input (dict): The Markov model to use for text generation.
    limit (int): The maximum number of words to generate.
    start (str): The initial state to start the text generation from.

    Returns:
    str: The generated text.
    """
    state_zero = start
    state_one = None
    text = state_zero + ' '
    for i in range(limit):
        state_one_dictionary = Counter(markov_model_input[state_zero])
        try:
            state_one = state_one_dictionary.most_common(10)[random.randint(0, 5)][0]
        except:
            state_one = state_one_dictionary.most_common(10)[0][0]
        text += state_one + ' '
        state_zero = state_one
    return text

# Callback to update the chapter text based on the selected chapter
@app.callback(Output('chapter-text', 'value'),
              [Input('pick_chapter', 'value')])
def update_chapter_text(chapter):
    """
    Update the chapter text based on the selected chapter.

    Parameters:
    chapter (str): The name of the selected chapter.

    Returns:
    str: The text of the selected chapter.
    """
    chapter_text_list = open(os.path.join(os.getcwd(), f'static/Data/sherlock/{chapter}')).readlines()
    chapter_text = ''.join(chapter_text_list)
    return chapter_text

# Load the Markov model from a JSON file
with open(os.path.join(os.getcwd(), f'static/Data/markov_model_JSON.txt')) as json_file:
    markov_model_json_to_dict = json.load(json_file)
    markov_model_json_to_dict = json.loads(markov_model_json_to_dict)


# Callback to update the generated text based on the input words and the number of clicks on the submit button
@app.callback(Output('generated-text', 'value'),
              [Input('choose_words', 'value'),
               Input('submit-val', 'n_clicks')])
def update_generated_text(words, n_clicks):
    """
    Update the generated text based on the input words and the number of clicks on the submit button.

    Parameters:
    words (str): The input words to start the text generation from.
    n_clicks (int): The number of clicks on the submit button.

    Returns:
    str: The generated text if the submit button was clicked, otherwise a message to click the submit button.
    """
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'submit-val.n_clicks' in changed_id:
        words = words.lower().strip()
        words = words + ' '

        generated_text = ''
        for i in range(10):
            generated_text += f's_{i + 1}' + ': ' + generate_text(markov_model_json_to_dict, start=words, limit=10) + '\n \n'

        return generated_text
    else:
        return 'Make sure you click on Submit button after writing two full words. ' \
               'Try different word combination if your input words are not present.'

# Run the Dash app server
if __name__ == '__main__':
    """
    Entry point for running the Dash app.

    Markov Chain Text Generation App:
    - Select a chapter from Sherlock Holmes book
    - Write two words in the text box
    - Click on Submit button to generate text based on the Markov Chain model
    - The generated text will appear in the second text box

    Markov chain is a stochastic model describing a sequence of possible events in which the probability of each event depends only on the state attained in the previous event. 
    In this app, the Markov chain is used to generate text based on the words from the selected chapter of Sherlock Holmes book. All the words from the selected chapter are used to create a Markov model.
    The Markov model is then used to generate text based on the input words. The generated text will be different each time the app is run.

    The Markov model is saved as a JSON file in the Data folder. The JSON file is loaded into a dictionary when the app is run.
    The Markov model is created using the following steps:
    - Read the text from the selected chapter
    - Split the text into words
    - Create a dictionary of words and their counts
    - Create a dictionary of words and their next words
    - Create a dictionary of words and their probabilities
    - Create a dictionary of words and their cumulative probabilities
    - Create a dictionary of words and their next words based on the probabilities
    - Save the Markov model as a JSON file

    Only top 5 most probable next words are used to generate text. This is done to avoid high randomness in the generated text.
    Also, a next word is selected randomly from the top 5 most probable next words to add some randomness to the generated text.
    Size of the text generated is limited to 50 words to avoid long text generation and can be changed in the generate_text function.

    """


    app.run_server(debug=True)