### Project Description
This is an interative python debugger or “Debugging Copilot” that helps students resolve Python errors and learn what went wrong. This system uses OpenAi, data science class slides and jupyter notebooks to provide students with hints to help them diagnose whats wrong with their code or provide class sources to lead students to the correct answer to solve their python coding issue.
### Installation Instructions
To run this project the following modules must be installed:
    ## Langchain
    pip install langchain
    pip install langchain-community
    pip install langchain-openai
    ## PDF Parsing
    pip install tika
    pip install pypdf
    ## Vector Database and Storage
    pip install chromadb
    ## Embeddings
    pip install sentence-transformers
    pip install huggingface-hub
    ## OpenAI Client
    pip install openai
    ## Others
    pip install python-dotenv
### Data Sources
This data comes from 2025 TKH data science classes. All data is intellectual property of TKH.
### Coding Structure
bug-a-boo/
│── slides/                        # Your input PDFs
│── .env                           # Holds API keys (OPENAI_API_KEY=xxxx)
│
├── prompt.py                      #Extracts PDFs, LLM calls for hints + tag extraction

### Results and Evaluation
To evaluate the performance of the model, a test set of 10–20 representative coding examples was constructed. Each example was designed to contain at least one error or debugging challenge that would prompt the generation of tiered hints. Model accuracy was assessed for: (1) the validity and usefulness of the hints produced at different tiers, measured by their ability to guide the learner toward identifying and correcting the error without prematurely revealing the solution, and (2) the ability of the pdf retrival component to correctly locate and return the most relevant class slides and page numbers, that aligned with the coding concept. Together, these criteria measured the quality of the model’s feedback and the reliability of the retrieved information.
## Future Work
To improve the functionality of the model we will continue to train and test the model for more accurate responses. To do this the evaluation dataset can be expanded to include a more diverse set of code snippets across different levels of difficulty. Additionally, improvements will also be made to refine tiered prompts and the vector database to increase the likelihood of surfacing the most relevant slides for a given error code. A nice to have would include system enhancements where the streamlit could be incorporated as an UI making it easier for students to paste code and visualize the slides for assistance.








