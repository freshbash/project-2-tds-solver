import os
from dotenv import load_dotenv
import httpx

INSTRUCTION = """
You will be given a assignment question and you have to parse it using the instruction that would be provided to you.
After parsing, you have to provide your answer as only the question ID and not other text.

For each given question, you have to provide a question ID based on a mapping that will be provided to you.
This mapping will have a ```key:value``` structure. For each key check if it is a substring of the question provided below, if yes, provide it's corresponding value, i.e. the question ID.

Finally provide the question id as your only output.

Here is the mapping that you will use to extract the question ID:

KEY: VALUE
"Install and run Visual Studio Code.": ga1q1
"Running uv run --with httpie -- https [URL]": ga1q2,
"Let's make sure you know how to use npx and prettier.": ga1q3,
"Let's make sure you can write formulas in Google Sheets": ga1q4,
"Let's make sure you can write formulas in Excel": ga1q5,
"Just above this paragraph, there's a hidden input with a secret value.": ga1q6,
"How many Wednesdays are there in": ga1q7,
"What is the value in the "answer" column of the CSV file?": ga1q8,
"Let's make sure you know how to use JSON": ga1q9,
"What's the result when you paste the JSON at tools-in-data-science.pages.dev/jsonhash and click the Hash button?": ga1q10,
"Let's make sure you know how to select elements using CSS selectors": ga1q11,
"Each file has 2 columns: symbol and value.": ga1q12,
"Let's make sure you know how to use GitHub. Create a GitHub account if you don't have one. Create a new public repository. Commit a single JSON file called email.json with the value {"email": "21f1004913@ds.study.iitm.ac.in"} and push it. Enter the raw Github URL of email.json so we can verify it. (It might look like https://raw.githubusercontent.com/[GITHUB ID]/[REPO NAME]/main/email.json.)": ga1q13,
"What does running cat * | sha256sum in that folder show in bash?": ga1q14,
"What's the total size of all files": ga1q15,
"What does running grep . * | LC_ALL=C sort | sha256sum in bash on that folder show?": ga1q16,
"How many lines are different between a.txt and b.txt?": ga1q17,
"There is a tickets table in a SQLite database": ga1q18,
"Write documentation in Markdown for an **imaginary** analysis": ga2q1,
"Download the image below and compress it losslessly": ga2q2,
"Is is question about publishing a GitHub Page?": ga2q3,
"Let's make sure you can access Google Colab": ga2q4,
"Download this image. Create a new Google Colab notebook and run this code": ga2q5,
"it returns a JSON response with the marks of the names X and Y in the same order": ga2q6,
"Create a GitHub action on one of your GitHub repositories. Make sure one of the steps in the action has a name that contains your email address 21f1004913@ds.study.iitm.ac.in. For example: jobs: test: steps: - name: 21f1004913@ds.study.iitm.ac.in run: echo "Hello, world!" Trigger the action and make sure it is the most recent action. What is your repository URL? It will look like: https://github.com/USER/REPO": ga2q7,
"Create and push an image to Docker Hub. Add a tag named 21f1004913 to the image.": ga2q8,
"If the URL has a query parameter class, it should return only students in those classes.": ga2q9,
"Create a tunnel to the Llamafile server using ngrok.": ga2q10,
"DataSentinel Inc. is a tech company specializing in building advanced natural language processing (NLP) solutions.": ga3q1,
"LexiSolve Inc. is a startup that delivers a conversational AI platform to enterprise clients.": ga3q2,
"RapidRoute Solutions is a logistics and delivery company": ga3q3,
"Acme Global Solutions manages hundreds of invoices from vendors every month": ga3q4,
"SecurePay, a leading fintech startup, has implemented an innovative feature": ga3q5,
"ShopSmart is an online retail platform that places a high value on customer feedback": ga3q6,
"InfoCore Solutions is a technology consulting firm that maintains an extensive": ga3q7,
"TechNova Corp. is a multinational corporation that has implemented a digital assistant": ga3q8,
"SecurePrompt Technologies is a cybersecurity firm": ga3q9,
"CricketPro Insights is a leading sports analytics firm": ga4q1,
"StreamFlix is a rapidly growing streaming service": ga4q2,
"GlobalEdu Platforms is a leading provider of educational technology solutions": ga4q3,
"AgroTech Insights is a leading agricultural technology company": ga4q4,
"Nominatim API": ga4q5,
"TechInsight Analytics is a leading market research firm": ga4q6,
"CodeConnect is an innovative recruitment platform": ga4q7,
"DevSync Solutions is a mid-sized software development company": ga4q8,
"EduAnalytics Corp. is a leading educational technology company": ga4q9,
"EduDocs Inc. is a leading provider of educational resources": ga4q10,
"RetailWise Inc. is a retail analytics firm": ga5q1,
"EduTrack Systems is a leading provider of educational management software": ga5q2,
"s-anand.net is a personal website that had region-specific music content. One of the site's key sections is kannada": ga5q3,
"s-anand.net is a personal website that had region-specific music content. One of the site's key sections is malayalammp3": ga5q4,
"GlobalRetail Insights is a market research and analytics firm": ga5q5,
"ReceiptRevive Analytics is a data recovery and business intelligence firm": ga5q6,
"DataSure Technologies is a leading provider of IT infrastructure": ga5q7,
"EngageMetrics is a digital marketing analytics firm": ga5q8,
"Mystery Tales Publishing is an independent publisher": ga5q9,
"PixelGuard Solutions is a digital forensics firm": ga5q10
"""

load_dotenv()

def query_openai(question):
    """Send a minimal request to OpenAI GPT-4o Mini."""
    headers = {"Authorization": f"Bearer eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIxZjEwMDQ5MTNAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.nbT1BzKJ4xz_LZM8jo4l_6957hbgC8cNHQHp0vLuZFc", "Content-Type": "application/json"}
    payload = {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": INSTRUCTION}, {"role": "user", "content": question}], "temperature": 0}
    
    try:
        response = httpx.post("http://aiproxy.sanand.workers.dev/openai/v1/chat/completions", json=payload, headers=headers)
        # print("RESPONSE>>>")
        # print(response)
        response.raise_for_status()
        result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No answer found.")
        if result == "No answer found.":
            raise Exception("Block 1 did not process the input correctly.")
        return result
    except Exception as e:
        return f"Error: {str(e)}"
