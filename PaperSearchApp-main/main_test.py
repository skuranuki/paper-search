import gradio as gr
import arxiv
from sentence_transformers import SentenceTransformer, util

# 論文情報を取得
def get_papers(query):
    papers = arxiv.query(query=query, max_results=10)
    return papers

# 文章をベクトル化
def embed_text(text):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    return model.encode(text, convert_to_tensor=True)

# 類似論文を検索
def search_similar_papers(query, input_text):
    papers = get_papers(query)
    input_vector = embed_text(input_text)
    similar_papers = []
    for paper in papers:
        title_vector = embed_text(paper['title'])
        similarity = util.pytorch_cos_sim(input_vector, title_vector)[0][0]
        similar_papers.append((paper['title'], similarity.item()))
    return sorted(similar_papers, key=lambda x: x[1], reverse=True)

# Gradioでアプリケーションを作成
def create_app():
    def search(query, input_text):
        similar_papers = search_similar_papers(query, input_text)
        return [f"{paper[0]} (類似度: {paper[1]:.2f})" for paper in similar_papers]

    iface = gr.Interface(
        fn=search,
        inputs=["text", "text"],
        outputs="text",
        title="論文検索アプリ",
        description="論文タイトルを入力して類似論文を検索します。",
    )
    iface.launch()

if __name__ == "__main__":
    create_app()