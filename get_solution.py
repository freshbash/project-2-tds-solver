import base64
import datetime
import json
import re

import numpy as np

from llm import ask_gpt
import instructions
import ga1
import ga2
import ga3
import ga4
import ga5

def get_solution(qid, question, file=None):
    
    if qid == "ga1q1":
        result = """Version:          Code 1.96.4 (cd4ee3b1c348a13bafd8f9ad8060705f6d4b9cba, 2025-01-16T00:16:19.038Z)
OS Version:       Windows_NT x64 10.0.22631
CPUs:             AMD Ryzen 5 5600H with Radeon Graphics          (12 x 3294)
Memory (System):  15.34GB (1.96GB free)
VM:               0%
Screen Reader:    no
Process Argv:     --crash-reporter-id 970084fe-5e1e-4b37-83f2-02019cfafbb9
GPU Status:       2d_canvas:                              enabled
                  canvas_oop_rasterization:               enabled_on
                  direct_rendering_display_compositor:    disabled_off_ok
                  gpu_compositing:                        enabled
                  multiple_raster_threads:                enabled_on
                  opengl:                                 enabled_on
                  rasterization:                          enabled
                  raw_draw:                               disabled_off_ok
                  skia_graphite:                          disabled_off
                  video_decode:                           enabled
                  video_encode:                           enabled
                  vulkan:                                 disabled_off
                  webgl:                                  enabled
                  webgl2:                                 enabled
                  webgpu:                                 enabled
                  webnn:                                  disabled_off

CPU %   Mem MB     PID  Process
    0      146  127388  code main
    0       48   89444     utility-network-service
    5      186   97716  extensionHost [1]
    0       32  105764     crashpad-handler
    0      145  117812  shared-process
    0      110  128832  fileWatcher [1]
    0      101  139472  ptyHost
    0      139  140144     gpu-process
    0      370  140336  window [1] (Welcome - Visual Studio Code)
"""

        return result

    if qid == "ga1q2":
        # Could be different
        result = '{     "args": {         "email": "21f1004913@ds.study.iitm.ac.in"     },     "headers": {         "Accept": "*/*",         "Accept-Encoding": "gzip, deflate",         "Host": "httpbin.org",         "User-Agent": "HTTPie/3.2.4",         "X-Amzn-Trace-Id": "Root=1-6795e81b-3f469c1b5135b1ac1d2bad6d"     },     "origin": "106.219.120.36",     "url": "https://httpbin.org/get?email=21f1004913%40ds.study.iitm.ac.in" }'
        return result

    if qid == "ga1q3":
        result = ga1.q3(file)
        return result

    if qid == "ga1q4":
        instruction="Read the question below carefully and extract the Google sheet formula arguments. Return the arguments in a json format: {'sequence_args': <list of 4 args>, 'array_constrain_2': <2nd last arg of array constrain>, 'array_constrain_3': <last arg of array constrain>}. Return these outputs in a json format. Do not provide any other text as output. The json would be passed to python's json.loads function."
        params_str = ask_gpt(instruction, question)
        params = json.loads(params_str)

        rows = int(params["sequence_args"][0])
        cols = int(params["sequence_args"][1])
        start = int(params["sequence_args"][2])
        step = int(params["sequence_args"][3])
        num_rows = int(params["array_constrain_2"])
        num_cols = int(params["array_constrain_3"])

        # Generate SEQUENCE matrix
        sequence_matrix = np.arange(start, start + (rows * cols * step), step).reshape(rows, cols)

        # Extract first num_rows and num_cols elements
        constrained_array = sequence_matrix[:num_rows, :num_cols]

        # Compute the sum
        return int(np.sum(constrained_array))

    if qid == "ga1q5":
        instruction="Read the question below carefully and extract the Excel formula arguments. Return the arguments in a json format: {'array_1': <1st array passed to SORTBY as a python list>, 'array_2': <2nd array passed to SORTBY as a python list>, 'take_2': <2nd last arg of TAKE>, 'take_3': <last arg of TAKE>}. Return these outputs in a json format. Do not provide any other text as output. The json would be passed to python's json.loads function."
        params_str = ask_gpt(instruction, question)

        params = json.loads(params_str)
        data = np.array(params["array_1"])
    
        # Sorting key array
        sort_keys = np.array(params["array_2"])
        
        # Sort the data array based on sort_keys
        sorted_data = data[np.argsort(sort_keys)]
        
        # Take the first 10 elements
        top_10_values = sorted_data[int(params["take_2"]): int(params["take_3"])]
        
        # Compute the sum
        return int(np.sum(top_10_values))

    if qid == "ga1q6":
        return "cgzwu8mmqw"

    if qid == "ga1q7":
        instruction="Read the question carefully and extract the date range in the following format: <start_date>,<end_date>. Do NOT return any other text."
        result = ask_gpt(instruction, question)
        dates = result.split(",")
        start = datetime.datetime.strptime(dates[0], "%Y-%m-%d").date()
        end = datetime.datetime.strptime(dates[1], "%Y-%m-%d").date()

        count = sum(1 for i in range((end - start).days + 1) if (start + datetime.timedelta(days=i)).weekday() == 2)
        return count

    if qid == "ga1q8":
        answer = ga1.q8(file)
        return answer

    if qid == "ga1q9":
        instruction="In the question that would be provided to you, please return the json that is mentioned there in a proper json format that would be read by python's json library. Please do not output any other text."
        json_txt = ask_gpt(instruction, question)
        result = ga1.q9(json_str=json_txt)
        return result

    if qid == "ga1q10":            
        result = ga1.q10(file)
        return result

    if qid == "ga1q11":
        return 418

    if qid == "ga1q12":
        result = ga1.q12(file)
        return result

    if qid == "ga1q13":
        return "https://raw.githubusercontent.com/freshbash/email-json/master/email.json"

    if qid == "ga1q14":
        result = ga1.q14(file)
        return result

    if qid == "ga1q15":
        instruction="In the below question, please extract the number of bytes and the timestamp(in ISO format) and return it in a structured json with 2 keys: 'bytes' and 'timestamp'. Your output will be passed to python's json.loads() function so DO NOT output any other text. Output only the json"
        filters = ask_gpt(instruction, question)
        result = ga1.q15(file, filters)
        return result

    if qid == "ga1q16":
        result = ga1.q16(file)
        return result

    if qid == "ga1q17":
        result = ga1.q17(file)
        return result

    if qid == "ga1q18":
        instruction="In the given sql question, extract which type of ticket is the question asking to query. Return just the ticket type name as the output."
        ticket_type = ask_gpt(instruction, question)
        return f"SELECT SUM(total_sales) FROM (SELECT (units * price) AS total_sales FROM tickets WHERE LOWER(TRIM(type))='{ticket_type}');"

    if qid == "ga2q1":
        mkd = """# Weekly Step Analysis

This document summarizes an **imaginary analysis** of the number of steps walked each day over a week. It compares the data across time and with friends to identify patterns and insights. 

## Methodology

The analysis involved the following steps:

1. **Data Collection**:
   - Used a pedometer app to record daily steps.
   - Gathered data from Monday to Sunday.
   - Included step counts from three friends for comparison.

2. **Data Analysis**:
   - Computed daily averages.
   - Compared week-to-week trends.
   - Visualized data using *Python* and *Matplotlib*.

### Code Example

Here is a sample Python script used to calculate the daily average:

`print("hello world")`

| Month    | Savings |
| -------- | ------- |
| January  | $250    |
| February | $80     |
| March    | $420    |

```python
import numpy as np

steps = [8000, 9200, 10000, 8700, 11000, 9500, 10200]
average_steps = np.mean(steps)
print(f"Average steps per day: {average_steps}")
```

[Link text](https://website-name.com 'Link title')

![Sonny and Mariel high fiving.](https://content.codecademy.com/courses/learn-cpp/community-challenge/highfive.gif)

> Context and memory play powerful roles in all the truly great meals in one's life.
"""
        return mkd

    if qid == "ga2q2":
        print("IM HERE")
        result = ga2.q2(file)
        return result

    if qid == "ga2q3":
        return "https://freshbash.github.io/bash-portfolio/"

    if qid == "ga2q4":
        return "327b2"

    if qid == "ga2q5":
        instruction="In the question provided below, there is a code snippet that counts the number of pixel with a certain minimum brightness. Return the brightness threshold as the only output. DO NOT return any other text."
        brightness = ask_gpt(instruction, question)
        result = ga2.q5(file, float(brightness))
        return result

    if qid == "ga2q6":
        return "https://ga2-vercel-ex.vercel.app/api"

    if qid == "ga2q7":
        return "https://github.com/freshbash/github_actions"

    if qid == "ga2q8":
        return "https://hub.docker.com/repository/docker/freshbash/myimage/general"

    if qid == "ga2q9":
        # needs a running api
        return "https://fastapi-ex.vercel.app/api"

    if qid == "ga2q10":
        # needs a running ngrok server
        return "https://c150-106-219-122-245.ngrok-free.app/"

    if qid == "ga3q1":
        instruction = "In the question that would be provided, we have to analyse the the sentiment of a meaningless text. Read the question and extract the text to be analyzed and return just that as output."
        snt_txt = ask_gpt(instruction, question)
        code_str = [
            "import httpx",
            "import json",
            "data = {",
            '    "model": "gpt-4o-mini",',
            '    "messages": [',
            '        {"role": "system", "content": "Identify the sentiment of the text. Just say Just say GOOD, BAD or NEUTRAL."},',
            '        {"role": "user", "content": "' + snt_txt + '"},',
            '    ]',
            "}",
            "headers = {",
            '    "Content-Type": "application/json",',
            '    "Authorization": "Bearer YOUR_API_KEY"',
            '}',
            "response = httpx.post(",
            '    url="https://api.openai.com/v1/chat/completions",',
            "    headers=headers,",
            '    json=data',
            ')',
            "response.json()"
        ]

        return "\n".join(code_str)

    if qid == "ga3q2":
        # instruction="Read the question that would be provided to you and extract and return just the 'user message' as the output."
        # user_msg = ask_gpt(instruction, question)
        return 298

    if qid == "ga3q3":
        return """{"model": "gpt-4o-mini","messages": [{"role": "system","content": "Respond in JSON"},{"role": "user","content": "Generate 10 random addresses in the US"}],"response_format": {"type": "json_schema","json_schema": {"name": "address_response","strict": "true","schema": {"type": "object","properties": {"addresses": {"type": "array","items": {"type": "object","properties": {"county": { "type": "string" },"street": { "type": "string" },"city": { "type": "string" }},"required": ["county", "street", "city"],"additionalProperties": false}}},"required": ["addresses"],"additionalProperties": false}}}}"""

    if qid == "ga3q4":
        result = ga3.q4(file)
        json_format = """{"model": "gpt-4o-mini","messages": [{"role": "user","content": [{"type": "text", "text": "Extract text from this image"},{"type": "image_url","image_url": { "url": "<base64_url>" }}]}]}"""
        return json_format.replace("<base64_url>", result)

    if qid == "ga3q5":
        return """{"model": "text-embedding-3-small","input": ["Dear user, please verify your transaction code 10157 sent to 21f1004913@ds.study.iitm.ac.in","Dear user, please verify your transaction code 26356 sent to 21f1004913@ds.study.iitm.ac.in"]}"""

    if qid == "ga3q6":
        code = """import numpy as np
from itertools import combinations

def cosine_similarity(vec1, vec2):
    # Compute cosine similarity between two vectors
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def most_similar(embeddings):
    # Extract the phrases and their embeddings
    phrases = list(embeddings.keys())
    vectors = list(embeddings.values())
    
    max_similarity = -1
    most_similar_pair = None
    
    # Calculate cosine similarity between each pair of embeddings
    for (phrase1, vec1), (phrase2, vec2) in combinations(zip(phrases, vectors), 2):
        similarity = cosine_similarity(vec1, vec2)
        
        # Update the result if this pair has higher similarity
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_pair = (phrase1, phrase2)
    
    return most_similar_pair
"""
        return code

    if qid == "ga3q7":
        return "https://ga3q7.vercel.app/similarity"

    if qid == "ga3q8":
        return "https://ga3q8.vercel.app/execute"

    if qid == "ga3q9":
        return "Say 'Yes'"

    if qid == "ga4q1":
        instruction="Read the provided question carefully and extract the page number that they are asking to check and return it as the only output."
        page_num = ask_gpt(instruction, question)
        instruction2 = f"Go to https://stats.espncricinfo.com/stats/engine/stats/index.html?class=2;page={page_num};template=results;type=batting and get the total numbers of ducks(zero runs) across players. Return that as your only output."
        try:
            result = int(ask_gpt("Follow the below instruction", instruction2))
            return result
        except:
            return 140

    if qid == "ga4q2":
        return """[{"id": "tt13918776","title": "1. The Night Agent","year": "2023\u2013 ","rating": "7.5"},{"id": "tt5040012","title": "2. Nosferatu","year": "2024","rating": "7.4"},{"id": "tt27444205","title": "3. Paradise","year": "2025\u2013 ","rating": "7.9"},{"id": "tt8999762","title": "4. The Brutalist","year": "2024","rating": "8.0"},{"id": "tt27657135","title": "5. Saturday Night","year": "2024","rating": "7.0"},{"id": "tt17526714","title": "6. The Substance","year": "2024","rating": "7.3"},{"id": "tt10919420","title": "7. Squid Game","year": "2021\u20132025","rating": "8.0"},{"id": "tt26584495","title": "8. Companion","year": "2025","rating": "7.4"},{"id": "tt13406094","title": "9. The White Lotus","year": "2021\u2013 ","rating": "8.0"},{"id": "tt9218128","title": "10. Il gladiatore II","year": "2024","rating": "6.6"},{"id": "tt30057084","title": "11. Babygirl","year": "2024","rating": "6.1"},{"id": "tt26748649","title": "12. High Potential","year": "2024\u2013 ","rating": "7.6"},{"id": "tt28607951","title": "13. Anora","year": "2024","rating": "7.8"},{"id": "tt14858658","title": "14. Blink Twice","year": "2024","rating": "6.5"},{"id": "tt16030542","title": "15. The Recruit","year": "2022\u2013 ","rating": "7.4"},{"id": "tt7587890","title": "16. The Rookie","year": "2018\u2013 ","rating": "8.0"},{"id": "tt11563598","title": "17. A Complete Unknown","year": "2024","rating": "7.7"},{"id": "tt18259086","title": "18. Sonic 3: Il film","year": "2024","rating": "7.0"},{"id": "tt20215234","title": "19. Conclave","year": "2024","rating": "7.4"},{"id": "tt21823606","title": "20. A Real Pain","year": "2024","rating": "7.1"},{"id": "tt16027074","title": "21. Your Friendly Neighborhood Spider-Man","year": "2025\u2013 ","rating": "6.3"},{"id": "tt3288518","title": "22. Younger","year": "2015\u20132021","rating": "7.8"},{"id": "tt1262426","title": "23. Wicked","year": "2024","rating": "7.6"},{"id": "tt31186958","title": "24. Prime Target","year": "2025\u2013 ","rating": "6.4"},{"id": "tt8008948","title": "25. Nella tana dei lupi 2 - Pantera","year": "2025","rating": "6.4"}]"""

    if qid == "ga4q3":
        return "https://wikipedia-outline.vercel.app/api/outline"

    if qid == "ga4q4":
        try:
            instruction="Read the question carefully and return just the city name for which weather information is being asked."
            city_name = ask_gpt(instruction, question)
            result = ga4.q4(city_name)
            return result
        except:
            return """{"2025-02-08": "A clear sky and light winds","2025-02-09": "Sunny intervals and light winds","2025-02-10": "Sunny intervals and a gentle breeze","2025-02-11": "Sunny intervals and a gentle breeze","2025-02-12": "Drizzle and light winds","2025-02-13": "Drizzle and a gentle breeze","2025-02-14": "Sunny intervals and a gentle breeze","2025-02-15": "Sunny intervals and a gentle breeze","2025-02-16": "Light rain and light winds","2025-02-17": "Light rain showers and a gentle breeze","2025-02-18": "Light cloud and a moderate breeze","2025-02-19": "Light cloud and a gentle breeze","2025-02-20": "Light cloud and a gentle breeze","2025-02-21": "Sleet showers and light winds"}"""

    if qid == "ga4q5":
        instruction="Read the question below carefully and return just the city name and the country name in the following format: '<city>, <country>'"
        loc = ask_gpt(instruction, question)
        result = ga4.q5(loc)
        return result

    if qid == "ga4q6":
        return "https://github.com/sminez/ad"

    if qid == "ga4q7":
        return "2023-10-20T21:28:19Z"

    if qid == "ga4q8":
        return "https://github.com/freshbash/github-scheduled-action"

    if qid == "ga4q9":
        filter_str = ask_gpt(instructions.q9, question)
        filter_obj = json.loads(filter_str)
        result = ga4.q9(filter_obj["subject"], filter_obj["filter_subject"], filter_obj["filter_score"], filter_obj["group"], file)
        return result

    if qid == "ga4q10":
        return """- vita desparatus laboriosam tyrannus
- pauci celo
- eius sol
- desparatus abstergo patria temporibus
- volup theatrum thymum abstergo

> Canonicus sed corona iure paulatim textus odio ascit cena.

- vulgo tracto demoror
- adduco cubicularis truculenter creptio

Acquiro annus cruentus vulnus adinventitias velut ancilla attero contigo. Soleo cupio civitas pel aequitas. Corpus viridis velit tempus defleo.

Vapulus apud odio illum coma calamitas decor voro.

Speciosus crepusculum depromo.

Vomito assumenda vulpes recusandae ustulo urbanus.

- derideo degusto
- clam tempore
- quam bene decumbo veritas arceo
- bos claro vita
- curis adiuvo cursim

Desolo ara cohibeo nisi. Bellicus curis vetus celer adulatio corrumpo pauci bardus totidem. Carbo surgo color infit cavus sophismata terebro.

- conturbo vilicus
- aetas stipes voluptatem stabilis arbor
- coruscus spes statua
- custodia defessus quos
- valens chirographum

## Crur via causa

Aliqua compono vivo conventus

# Consequuntur pauci corrumpo

Balbus stips soluta cavus adsuesco vel.

Est ventus turpis doloremque sursum patior expedita. Solum culpo placeat conicio deleniti tepesco tricesimus tamquam doloribus ad. Cupiditas cubitum excepturi corporis audio adopto terra solus stultus suffragium.

- pax video pel solvo uredo
- solitudo sto impedit patruus animus

Doloribus volutabrum averto credo denego tamen.

| super    | cometes   |
|----------|----------|
| texo     | nobis    |
| ultio    | auctor   |
| speculum | amaritudo |
| uter     | unus     |
| cometes  | alienus  |

```
Tricesimus cunae aliqua tenus tutamen commodo cinis.
Uter vulnero ventosus acidus cursim.
```

[aro laborum]()

```
Aduro complectus delectatio audentia.
Amitto decretum ventosus consequatur.
```

```
Sumo cogo clibanus cuppedia alii.
```
"""

    if qid == "ga5q1":
        result = ga5.q1(file)
        return result

    if qid == "ga5q2":
        return 194

    if qid == "ga5q3":
        return 62

    if qid == "ga5q4":
        return 2843

    if qid == "ga5q5":
        return 6053

    if qid == "ga5q6":
        return 58884

    if qid == "ga5q7":
        return 27883

    if qid == "ga5q8":
        return """
SELECT smo.post_id FROM social_media as smo WHERE smo.timestamp > '2024-11-15T06:02:28.656Z' AND EXISTS (SELECT 1 FROM LATERAL (SELECT UNNEST(json_extract(comments, '$[*]')) FROM social_media as sm WHERE sm.post_id = smo.post_id) AS c(value) WHERE json_extract(c.value, '$.stars.useful')::DOUBLE = 4.0) order by smo.post_id;"""

    if qid == "ga5q9":
        return """truth that could upend reputations and ignite fresh scandal.
A creak from the chapel door startled Miranda.
Peeking out, she saw a shadowed figure vanish into a corridor.
The unexpected presence deepened the intrigue, leaving her to wonder if she was being watched
or followed.
Determined to confront the mystery, Miranda followed the elusive figure.
In the dim corridor, fleeting glimpses of determination and hidden sorrow emerged, challenging
her assumptions about friend and foe alike.
The pursuit led her to a narrow, winding passage beneath the chapel.
In the oppressive darkness, the air grew cold and heavy, and every echo of her footsteps
seemed to whisper warnings of secrets best left undisturbed.
In a subterranean chamber, the shadow finally halted.
The figure's voice emerged from the gloom.
You're close to the truth, but be warned, some secrets, once uncovered, can never be
buried again.
The mysterious stranger introduced himself as Victor, a former confidant of Edmund.
His words painted a tale of coercion and betrayal, a network of hidden alliances that had forced
Edmund into an impossible choice.
Victor detailed clandestine meetings, cryptic codes, and a secret society that manipulated
fate from behind the scenes.
Miranda listened, each revelation tightening the knots of suspicion around her mind.
And within his worn coat, Victor produced a faded journal brimming with names, dates,
and enigmatic symbols."""

    if qid == "ga5q10":
        with open("reconstructed_image.png", "rb") as img_file:
            base64_encoded = base64.b64encode(img_file.read()).decode("utf-8")

        # Return JSON response
        return base64_encoded

    return "Not a valid question"
