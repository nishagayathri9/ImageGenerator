# imports
import streamlit as st
from openai import OpenAI

st.header('The Ultimate Image Generator', divider='rainbow')

# variables
api_key = st.secrets['openai_secret']
client = OpenAI(api_key=api_key)

# methods 
def generate_story(prompt):
  story_response = client.chat.completions.create(
      model = 'gpt-3.5-turbo',
      messages = [{
          'role': 'system',
          'content': 'You are a bestseller story writer.You will take users prompt and generate a 100 words short story for adults age 20-30.'
      },
      {
          'role': 'user',
          'content': f'{prompt}'
      }],
      max_tokens = 400,
      temperature = 0.8
  )

  story = story_response.choices[0].message.content
  return story 

def refine_prompt(prompt):
  design_response = client.chat.completions.create(
      model = 'gpt-3.5-turbo',
      messages = [{
          'role': 'system',
          'content': 'Based on the story given,you will design a detailed image prompt for the cover image for this story. The image prompt should include the theme of the story with the relevant color, and aesthetic suitable for adults. The output should be within 100 characters and show be very detailed.'
      },
      {
          'role': 'user',
          'content': f'{story}'
      }],
      max_tokens = 400,
      temperature = 0.8
  )

  design_prompt = design_response.choices[0].message.content
  return design_prompt

def create_image(design_prompt):
  cover_response = client.images.generate(
      model = 'dall-e-3',
      prompt = f"{design_prompt}" ,
      size = '1024x1024',
      quality = 'standard',
      n = 1,
  )

  image_url = cover_response.data[0].url
  return image_url

# run methods

with st.form('story_form'):
  st.write('Enter your prompt here')
  msg = st.text_input(label="Input")
  submitted = st.form_submit_button(label="Submit")

  if submitted:
      story = generate_story(msg)

      prompt = refine_prompt(story)
    
      image_url = create_image(prompt)
      st.image(image_url)