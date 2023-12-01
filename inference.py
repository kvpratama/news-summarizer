import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer "}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query({
    "inputs": "Emily had been at a sleepover at Hila’s house when Hamas terrorists stormed Kibbutz Be’eri. Hand was trapped in his house for hours, unable to reach his daughter, as the community was ravaged – about 130 residents killed and others captured. About two days later, he was told by kibbutz leaders Emily’s body had been seen. He told CNN: “They just said, ‘We found Emily. She’s dead.’ And I went, ‘Yes!’ I went, ‘Yes!’ and smiled because that is the best news of the possibilities that I knew … So death was a blessing, an absolute blessing. But nearly a month later, the Israeli army told him it was “highly probable” Emily was alive and a hostage of Hamas. Hand said the military had been piecing together bits of information and intelligence. None of the remains at Kibbutz Be’eri were identified as those of Emily. There was no blood in the house where she slept. And cellphones belonging to Hila’s family had been tracked to Gaza.From feeling that death would be a blessing, he now had all the fear of the conditions Emily was being held in. “The unknown is awful. The waiting is awful,” he told CNN while she was a captive. But there was also some hope.",
})

print(output)
