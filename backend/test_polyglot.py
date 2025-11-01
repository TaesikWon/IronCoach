from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "EleutherAI/polyglot-ko-1.3b"

print("🔹 모델 로딩 중... (최초 1회는 다소 오래 걸릴 수 있음)")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto"
)

prompt = "오늘 하체 운동 루틴을 추천해줘."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

# 🔧 모델이 이해 못 하는 token_type_ids 제거
inputs.pop("token_type_ids", None)

outputs = model.generate(**inputs, max_new_tokens=150)

print("\n✅ 결과:")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
