from transformers import BertForSequenceClassification, BertTokenizer
import torch
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')
if torch.cuda.is_available():
    device = ("cuda")
else:
    device = torch.device("cpu")
# device = torch.device("cpu")
print(device)
# df = pd.read_csv("/kaggle/input/cleaned-dataset/cleaned.csv")
def get_sentiment(txt):
	tokens = tokenizer.encode_plus(txt, add_special_tokens=False, return_tensors='pt')
	# print(len(tokens))
	# print("tokens",tokens)
	# print(len(tokens['input_ids'][0]))
	input_id_chunks = tokens['input_ids'][0].split(510)
	attention_mask_chunks = tokens['attention_mask'][0].split(510)

	# print(len(attention_mask_chunks))
	# print(len(attention_mask_chunks[0]))
	# print(input_id_chunks[0].shape)
	def get_input_ids_and_attention_mask_chunk():

		chunksize = 512
		input_id_chunks = list(tokens['input_ids'][0].split(chunksize - 2))
		attention_mask_chunks = list(tokens['attention_mask'][0].split(chunksize - 2))

		for i in range(len(input_id_chunks)):
			input_id_chunks[i] = torch.cat([
				torch.tensor([101]).to(device), input_id_chunks[i].to(device), torch.tensor([102]).to(device)])
			attention_mask_chunks[i] = torch.cat([
				torch.tensor([1]).to(device), attention_mask_chunks[i].to(device), torch.tensor([1]).to(device)])
			pad_length = chunksize - input_id_chunks[i].shape[0]
			if pad_length > 0:
				input_id_chunks[i] = torch.cat([
					input_id_chunks[i], torch.Tensor([0] * pad_length).to(device)
				])
				attention_mask_chunks[i] = torch.cat([
					attention_mask_chunks[i], torch.Tensor([0] * pad_length).to(device)
				])

		return input_id_chunks, attention_mask_chunks

	input_id_chunks, attention_mask_chunks = get_input_ids_and_attention_mask_chunk()
	input_ids = torch.stack(input_id_chunks)
	attention_mask = torch.stack(attention_mask_chunks)

	input_ids = input_ids.to(device)
	attention_mask = attention_mask.to(device)
	model.to(device)

	input_dict = {
		'input_ids': input_ids.long(),
		'attention_mask': attention_mask.int()
	}
	# print("input dict: ",input_dict)
	# print(input_dict['input_ids'].shape)
	# print(input_dict['attention_mask'].shape)
	outputs = model(**input_dict)
	probabilities = torch.nn.functional.softmax(outputs[0], dim=-1)
	mean_probabilities = probabilities.mean(dim=0)

	# print(mean_probabilities)

	dict_ref = {0: "positive", 1: "negative", 2: "nuetral"}
	return dict_ref[torch.argmax(mean_probabilities).item()]


# print(get_sentiment("""Shares of TVS Motor Company rose over 7% today after the auto firm reported a 9 per cent rise in its net profit for the quarter ended December. TVS Motor Company stock climbed 7.57% to Rs 685 against the previous close of Rs 636.80 on BSE. The stock has gained after two days of consecutive fall. TVS Motor Company share is trading higher than 5 day, 20 day, 50 day, 100 day and 200 day moving averages. The stock has gained 1.8% in a year and risen 3.92% since the beginning of this year. Market cap of the firm stood at Rs 30,761 on BSE. Total 2.26 lakh shares of the firm changed hands amounting to a turnover of Rs 14.71 crore. Stock Market LIVE: Sensex falls over 100 pts; PowerGrid, L&T, Kotak Bank top losers The large cap stock hit a 52-week high of Rs 793.45 on November 9, 2021 and a 52 week low of Rs 495 on August 24, 2021. The two-wheeler firm reported a 9 per cent rise in its net profit to Rs 288.31 crore in Q3 against a net profit of Rs 265.62 crore in the year-ago. The company also clocked its highest ever profit before tax of Rs 391 crore in the last quarter. It reported highest ever operating revenue of Rs 5,706 crore in the Q3FY22 as against Rs 5,391crore in the corresponding quarter of previous fiscal. The company's operating earnings before interest, taxes, depreciation, and amortization or EBITDA margin stood at 10 per cent during the quarter as against 9.5 per cent during the third quarter ended December 2020, while it registered highest-ever EBITDA of Rs 568 crore during this quarter as against Rs 511 crore reported in the quarter ended December 2020, TVS Motor company said in a regulatory filing. ICICI Securities has maintained a buy call on the stock after Q3 earnings. "We continue to like TVS Motor's capability of delivering industry-leading growth on the back of strong product offerings with aggressive capital deployment into EVs and a portfolio of products that reflect well on its confidence to scale up manufacturing. Factoring-in the SEMG acquisition, we trim our earnings by 5%/2.2% for FY23E/FY24E and value the stock on DCF basis at Rs776/share (earlier: Rs792) at 21x FY24E core EPS, including Rs48/share of captive NBFC. Maintain BUY," said the brokerage. Yes Securities too has maintained a buy stance on the stock and expects the stock to climb 19% against the current market price of Rs 637. "EV focus continues to intensify with more capex/investments towards the same. We believe sustained market share gains in domestic EV 2Ws led by aggressive product pipeline, scope of external investments in to EV vertical and NBFC TVS credit are additional re-rating triggers. We therefor retain BUY with TP of Rs 759 (v/s Rs760) with FY23/24 estimates largely remaining unchanged," the brokerage said.
# """))



def tfidf_summarize(input_text):
    # Tokenizing the text
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(input_text)

    # Creating a frequency table to keep the score of each word
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    # Creating a dictionary to keep the score of each sentence
    sentences = sent_tokenize(input_text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    # Average value of a sentence from the original text
    average = int(sumValues / len(sentenceValue))

    # Storing sentences into our summary.
    summary = ''
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence

    return summary

# Example usage:
