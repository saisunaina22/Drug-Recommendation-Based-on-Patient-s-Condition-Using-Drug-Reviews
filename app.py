
from flask import Flask, render_template, request
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Load the dataset
df = pd.read_csv("processed_medical_reviewsm.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    reviews = []
    wordcloud_generated = False
    search_condition = ""
    if request.method == "POST":
        search_condition = request.form.get("condition", "").lower()
        filtered_df = df[df['condition'].str.lower().str.contains(search_condition, na=False)]
        
        reviews = filtered_df[['drugName', 'review', 'rating']].to_dict(orient="records")[:20]
        
        text = " ".join(filtered_df['review'].astype(str).tolist())
        if text.strip():
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            wordcloud.to_file("static/wordcloud.png")
            wordcloud_generated = True
    
    return render_template("index.html", reviews=reviews, wordcloud_generated=wordcloud_generated, condition=search_condition)

@app.route("/insights")
def insights():
    total_reviews = len(df)
    top_conditions = df['condition'].value_counts().head(10)
    ratings_dist = df['rating'].value_counts().sort_index()
    useful_count_dist = df['usefulCount'].clip(upper=50).value_counts().sort_index()
    
    plt.figure(figsize=(10,6))
    top_conditions.plot(kind='bar', color='skyblue')
    plt.title("Top 10 Conditions")
    plt.ylabel("Number of Reviews")
    plt.tight_layout()
    plt.savefig("static/top_conditions.png")
    plt.close()
    
    plt.figure(figsize=(10,6))
    ratings_dist.plot(kind='bar', color='lightgreen')
    plt.title("Ratings Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("static/ratings_distribution.png")
    plt.close()
    
    plt.figure(figsize=(10,6))
    useful_count_dist.plot(kind='bar', color='salmon')
    plt.title("UsefulCount Distribution (clipped at 50)")
    plt.xlabel("UsefulCount")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("static/usefulcount_distribution.png")
    plt.close()
    
    return render_template("insights.html", total_reviews=total_reviews)

if __name__ == "__main__":
    app.run(debug=True)
