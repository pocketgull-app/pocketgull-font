"""
train_qlora_gemma.py
====================
Clean SFT QLoRA trainer targeting `google/gemma-3-1b-it` on the synthetic
PocketGull Prosody JSONL dataset (`data/train.jsonl`, `data/eval.jsonl`).
Intended for isolated GPU training (Google Colab T4/L4, Kaggle, or Linux ROCm container).
"""

import argparse
import os
from datasets import load_dataset
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTConfig, SFTTrainer


def main():
    parser = argparse.ArgumentParser(description="Fine-tune google/gemma-3-1b-it for PocketGull Prosody JSON keyframes")
    parser.add_argument("--base_model", default="google/gemma-3-1b-it")
    parser.add_argument("--train_file", default=os.path.join(os.path.dirname(__file__), "data", "train.jsonl"))
    parser.add_argument("--eval_file", default=os.path.join(os.path.dirname(__file__), "data", "eval.jsonl"))
    parser.add_argument("--output_dir", default="./pocketgull-prosody-gemma-3-1b-lora")
    parser.add_argument("--epochs", type=int, default=4)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--push_to_hub", default="")
    args = parser.parse_args()

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        quantization_config=bnb_config,
        device_map="auto",
        attn_implementation="eager",
    )
    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, lora_config)

    dataset = load_dataset("json", data_files={"train": args.train_file, "validation": args.eval_file})

    sft_config = SFTConfig(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        learning_rate=args.lr,
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        bf16=torch.cuda.is_bf16_supported(),
        fp16=not torch.cuda.is_bf16_supported(),
        max_length=1024,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        args=sft_config,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
    )

    trainer.train()
    merged = trainer.model.merge_and_unload()
    merged_dir = args.output_dir + "-merged"
    merged.save_pretrained(merged_dir, safe_serialization=True)
    tokenizer.save_pretrained(merged_dir)

    if args.push_to_hub:
        merged.push_to_hub(args.push_to_hub)
        tokenizer.push_to_hub(args.push_to_hub)

    print(f"Saved merged Gemma prosody model to: {merged_dir}")


if __name__ == "__main__":
    main()
