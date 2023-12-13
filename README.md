# NLP Group Project with Russell - COMP 482

This project focuses on Natural Language Processing (NLP) applications, utilizing various GPT models, a custom model which was fine-tuned using FAQ data from gigabytes website and a custom GUI. It was developed as part of the COMP 482 course.

---

## Installation

### Clone the repository

```bash
git clone https://github.com/BrianAtkinson93/COMP_482_NLP_Group_Project.git
```

#### Create Virtual Environment
> Windows
>```bash
>python3.exe -m venv venv
>```
>Linux
>```bash
>python3 -m venv venv
>```

#### Install required dependencies

```bash
# Source the virtual environment then:
pip install -r requirements.txt;
```

---

# Usage

---

##### To run the GUI simply run main.py:

### WINDOWS
```bash
# For help message and expected arguments
python.exe main.py -h

#usage: main.py [-h] [-a-] [-m {1,2,3,4,5}]
#
#options:
#  -h, --help            show this help message and exit
#  -a-, --api            Use this flag to run with the OpenAI API model.
#  -m {1,2,3,4,5}, --model {1,2,3,4,5}
#                        Choose a model number for the local GPT4All model. (Default is 5)
```
```bash
# Main program execution

python.exe main.py
```

```bash
# Optional model selection
python.exe main.py --model <1-5>
```

```bash
# For use with an API to GPT4
python3 main.py --api
```
### LINUX 
```bash
# For help message and expected arguments
python3 main.py -h

#usage: main.py [-h] [-a-] [-m {1,2,3,4,5}]
#
#options:
#  -h, --help            show this help message and exit
#  -a-, --api            Use this flag to run with the OpenAI API model.
#  -m {1,2,3,4,5}, --model {1,2,3,4,5}
#                        Choose a model number for the local GPT4All model. (Default is 5)
```
```bash
# Main program execution

python3 main.py
```

```bash
# Optional model selection
python3 main.py --model <1-5>
```

```bash
# For use with an API to GPT4
python3 main.py --api
```
# Contributors
> * Brian Atkinson - Main Infrastructure, GUI, Scrapper
> * Mason Leitch - Custom model training, Fine-Tuning, Quantization
> * Ayyan Momin
> * Owen Gossen - Testing, file conversion, Presentation

# License

This project includes third-party components under their respective licenses:

- **Selenium**: Licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0). For more details, see [CC BY-SA 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

- **GPT-4 Models (GGUF models) from gpt4all.io**: The licensing terms for these models should be reviewed at [gpt4all.io](https://gpt4all.io/index.html).

- **QLoRA**: QLoRA finetuning is licensed under MIT license. [QLoRA github repository](https://github.com/artidoro/qlora).

- **Llama.cpp**: Llama.cpp is licensed under MIT license. [Llama.cpp github repository](https://github.com/ggerganov/llama.cpp).

- **WizardLM 7B**: WizardLM 7B is non commercially licensed. [WizardLM-7B-V1.0](https://huggingface.co/WizardLM/WizardLM-7B-V1.0).
