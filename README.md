# Notion Assistant
This takes your notion and allows you to ask questions about it. 
Example of `advanced_query.py`:
```
Ask a question about yourself: What is my ideal daily routine? Please start from 8am EST to 11pm EST, and create a schedule.
===== BREAKING DOWN ORIGINAL QUESTION =====
--- Breaking down What is my ideal daily routine? Please start from 8am EST to 11pm EST, and screate a schedule. ---
 What are my personal goals and priorities?
 How much time and energy do I have available during this timeframe?
 What tasks and activities are essential and non-negotiable for me?
------------------------
===== ANSWERING SUBQUESTIONS WITH REFERENCES =====
--- Answering  What are my personal goals and priorities? ---
Based on the documents provided, your personal goals and priorities include:

1. Career advancement and planned fun.
2. Creating a community for the lifestyle you want to live.
3. Improving focus and speed at work, as well as enhancing temporal control and flow in conversations.
4. Prioritizing physical health, personal wealth and freedom, and nurturing relationships.
        ...

It's important to note that these goals may evolve and change over time as you gain new experiences and insights. Take the time to regularly reassess and adjust your priorities based on what truly brings you fulfillment and happiness.
------------------------
--- Answering  How much time and energy do I have available during this timeframe? ---
Based on the notes provided, it seems that time and energy are considered as similar resources. The notes mention that money saves time and energy, and that the more time you spend, the more energy you lose. It also suggests that planning helps avoid resentment towards people. To determine how much time and energy you have available during this timeframe, you can start by considering factors such as your current status, assets you have (including time and energy), and how you choose to allocate your resources. You may need to budget these resources weekly to ensure efficient use.
------------------------
--- Answering  What tasks and activities are essential and non-negotiable for me? ---
Based on the provided notes, the essential and non-negotiable tasks and activities for you are:

1) Navigating conversations with lightheartedness and emotion-evoking qualities.
2) Admitting when you are wrong.
3) Breathing, thinking, and taking action.
4) Engaging in activities you enjoy.
        ...
------------------------
===== ANSWERING ORIGINAL QUESTION BASED ON DEDUCTIONS =====
--- SYNTHESIS ---
Ideal Daily Routine (8am EST to 11pm EST):

8am-9am: Morning routine including meditation and exercise.
9am-12pm: Focus on work, enhancing speed and focus.
12pm-1pm: Break for a healthy lunch and socializing.
1pm-5pm: Continue work, prioritize tasks, and engage in conversations.
5pm-7pm: Engage in activities that bring fulfillment and happiness.
7pm-8pm: Dinner and relaxation time.
8pm-10pm: Pursue personal interests, like learning languages and blogging.
10pm-11pm: Wind down with reading and reflection before bedtime.
------------------------

```

## Setup
0. Install requirements.txt: `pip install -r requirements.txt`
1. Get a Notion api key and create an integration: https://developers.notion.com/docs/getting-started
2. For every page you want to use as reference, manually add the connection to the page ('...' on top right, under Connections). Note that if you add a top-level page, all the sub-pages will be automatically included.
3. Get an Open AI api key: https://openai.com/blog/openai-api
4. Add your API keys to a .env file
5. Run `python fetch_pages.py`. This will store embeddings and text snippets as a csv. 
6. Run `python advanced_query.py`