import gradio as gr
import pickle


chat_history = []

# Load the models
with open("models/textclassifier_sentiment.pickle", "rb") as file:
    classifierKNN = pickle.load(file)

with open("models/tfidfmodel.pickle", "rb") as file:
    vectorizer = pickle.load(file)


def predict_sentiment(text):
    # Convert the text into a numerical representation
    numerical_representation = vectorizer.transform([text])
    
    # Predict the sentiment of the text
    predicted_sentiment = classifierKNN.predict(numerical_representation)
    
    # Return the predicted sentiment
    return "Positive" if predicted_sentiment[0] == 1 else "Negative"


with gr.Blocks(title="Sentiment Analysis") as app:
    gr.Markdown("# Sentiment Analysis")
    gr.Markdown("Enter a sentence to predict its sentiment. The model predicts whether the sentiment is positive or negative.")

    chatbot = gr.Chatbot()
    input_msg = gr.Textbox()
    gr.ClearButton([input_msg, chatbot])

    def respond(message, chat_history):
        bot_message = predict_sentiment(message)
        chat_history.append((message, bot_message))
        return "", chat_history

    input_msg.submit(respond, [input_msg, chatbot], [input_msg, chatbot])


if __name__ == "__main__":
    app.launch(server_name="0.0.0.0")