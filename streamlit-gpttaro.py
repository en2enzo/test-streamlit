import io
import streamlit as st
import openai
from openai import OpenAI
import os

st.title(":bearded_person:言い聞かせGPT太郎")

st.sidebar.title("※注意：　GPT-4oとtts-1モデルのAPI利用料金がかかります。")
api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY") or "")
st.sidebar.write("APIキーが漏洩した場合に備えて定期的にAPIキーはローテーションすることをお勧めします")

if not api_key:
    st.warning("サイドバーからAPIキーを入力してください。")
    st.stop()
else:
    #os.environ["OPENAI_API_KEY"] = api_key
    openai.api_key = api_key



client = OpenAI(api_key=api_key)


def stream_and_play(text,voice):
    response = client.audio.speech.create(
        model="tts-1",
        #voice="alloy",
        voice=voice,
        input=text,
    )

    audio_bytes = response.content
    return audio_bytes

def chat_openai(text):
    template=f"""
    子供が言うこと聞かないので困っています。以下の困りごとに対して、小学生向けに言うことを言い聞かせる雰囲気で関西弁で落語風に１０００文字くらいで文章を作って優しく言ってください。
    １人の子供向けに話をしてください。
    回答する文章には「落語風」や「関西弁」とは出力しないでください。
    markdown形式でお願いします。会話の部分「」の文章は太字にしてください。
    ＃＃＃困りごと
    {text}
    """
    #１人の子供に向けて話をしてください。
    #次の質問に対して回答してください。
    #＃＃＃質問
    #{text}

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": template}

        ]
    )
    ans = completion.choices[0].message.content
    return ans



st.markdown("### 困りごとを教えてください。例：「子供が早く寝なくて困っています」")

if prompt := st.chat_input("困りごとを入力してください"):
    st.chat_message("user", avatar="./woman-raising-hand.png").write(prompt)

    with st.spinner("GPT太郎さんに問い合わせ中です。少しお待ちください..."):
        text_res = chat_openai(prompt)
        st.subheader("GPT太郎さんからお子様へのメッセージ")
        #st.write(text_res)
        #st.chat_message("assistant").write(text_res)
        #st.chat_message("assistant", avatar=":bearded_person:").write(text_res)
        st.chat_message("assistant", avatar="./bearded_person.png").write(text_res)
        #-------回答文章---------------------#
    with st.spinner("GPT太郎さんの音声を生成中です。少しお待ちください..."):
        audio_bytes = stream_and_play(text_res, "onyx")
        st.subheader("GPT太郎さんから音声をお聞きください")
        st.audio(audio_bytes, format='audio/mp3')
