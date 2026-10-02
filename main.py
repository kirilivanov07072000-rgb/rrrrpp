import io
import os
import cv2
import numpy as np
import requests
import streamlit as st
from PIL import Image

st.set_page_config(page_title="AI Studio & Smart Photo Editor", layout="wide")

HF_TOKEN = "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"


def generate_image(prompt):
  try:
    api_url = "https://router.huggingface.co/hf-inference/v1/models/black-forest-labs/FLUX.1-schnell"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"inputs": prompt}

    response = requests.post(api_url, headers=headers, json=payload, timeout=30)

    if response.status_code == 200:
      return response.content, None
    elif response.status_code == 401:
      return None, "Неверный или недействительный API-токен Hugging Face."
    else:
      return None, f"Ошибка сервера ({response.status_code}): {response.text}"
  except requests.exceptions.Timeout:
    return None, "Превышено время ожидания ответа (Timeout)."
  except Exception as e:
    return None, f"Ошибка соединения: {e}"


if "current_image" not in st.session_state:
  st.session_state["current_image"] = None

st.title("AI Studio & Smart Photo Editor")

st.header("1. Генерация изображения через AI")

prompt = st.text_area("Опишите изображение, которое хотите создать:")

STYLES = {
    "Без стиля": "",
    "Реалистичный": ", high detail, photorealistic, natural lighting",
    "Акварель": ", watercolor painting style, soft edges, pastel colors",
    "Мультяшный": ", 3D animated movie style, vibrant colors, friendly look",
    "Пиксель-Арт": ", pixel art style, 16-bit retro game aesthetic",
}

styles_choice = st.selectbox("Выберите стиль:", list(STYLES.keys()))

if st.button("Сгенерировать изображение"):
  if prompt.strip():
    final_prompt = prompt + STYLES[styles_choice]
    with st.spinner("AI создает изображение..."):
      image_bytes, error = generate_image(final_prompt)

    if error:
      st.error(f"Не удалось сгенерировать изображение: {error}")
    elif image_bytes:
      try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        st.session_state["current_image"] = img
        st.success("Изображение успешно сгенерировано!")
      except Exception as e:
        st.error(f"Не удалось открыть полученный файл как изображение: {e}")
  else:
    st.warning("Пожалуйста, введите промпт перед генерацией.")

st.divider()

st.header("2. Выбор источника изображения")

source_option = st.radio(
    "Выберите, какое изображение редактировать:",
    ["Сгенерированное ИИ", "Загрузить свое фото"],
    horizontal=True,
)

image_to_process = None

if source_option == "Сгенерированное ИИ":
  if st.session_state["current_image"] is not None:
    image_to_process = st.session_state["current_image"]
  else:
    st.info("Сначала сгенерируйте изображение с помощью AI выше.")
else:
  uploaded_file = st.file_uploader(
      "Выберите файл на компьютере:", type=["png", "jpg", "jpeg"]
  )
  if uploaded_file is not None:
    image_to_process = Image.open(uploaded_file).convert("RGB")

if image_to_process is not None:
  st.sidebar.header("Настройки фильтров")

  filter_option = st.sidebar.selectbox(
      "Эффект:",
      [
          "Без эффектов",
          "Серость",
          "Размытость",
          "Яркая вспышка",
          "Инверсия",
          "Развёрнутый",
      ],
  )

  img_array = np.array(image_to_process)
  processed_img = img_array.copy()

  if filter_option == "Серость":
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    processed_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
  elif filter_option == "Размытость":
    processed_img = cv2.GaussianBlur(img_array, (15, 15), 0)
  elif filter_option == "Яркая вспышка":
    processed_img = cv2.convertScaleAbs(img_array, alpha=1.0, beta=50)
  elif filter_option == "Инверсия":
    processed_img = 255 - img_array
  elif filter_option == "Развёрнутый":
    processed_img = cv2.flip(img_array, 1)

  col1, col2 = st.columns(2)

  with col1:
    st.subheader("Оригинал")
    st.image(img_array, use_container_width=True)

  with col2:
    st.subheader("Обработанное фото")
    st.image(processed_img, use_container_width=True)

    result_img = Image.fromarray(processed_img)
    buf = io.BytesIO()
    result_img.save(buf, format="JPEG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Сохранить результат",
        data=byte_im,
        file_name="edited_image.jpeg",
        mime="image/jpeg",
    )