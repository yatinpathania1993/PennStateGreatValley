# PennStateGreatValley
![image](https://github.com/user-attachments/assets/50e5cf59-d99a-4743-b3ef-7e196322146a)

This project is designed to scrape, process, and analyze static and dynamic web data for Penn State Great Valley. It collects information across multiple tabs such as Academics, Admissions, Professional Development, and Information For, and organizes it into vector databases. The system enables semantic search and efficient query answering through a unified vector database and LangChain-powered agents.

---

## **Features**

### **1. Data Collection**
- **Static Data Scraping:**
  - Webpages are scraped using BeautifulSoup.
  - The content is hashed using SHA-256 to detect changes when pages are updated.
  - The scraped data is stored in `.txt` files for further processing.
- **Dynamic Data Scraping:**
  - Compares hash values from previously stored data to detect updated pages dynamically.
  - If changes are detected, the updated content is processed and stored.
  
### **2. Metadata Structure**
Each page's metadata includes:
- `Page_Name`: Name of the webpage.
- `Link`: URL of the webpage.
- `Hash_Code`: SHA-256 hash value of the page content to detect updates.
- `Old_Hash_Code`: Previous hash value (for comparison in dynamic updates).

### **3. Vector Database Creation**
- **Chunking Documents:**
  - Text from `.txt` or `.pdf` files is split into smaller chunks using LangChain's RecursiveCharacterTextSplitter for efficient processing.
- **Embedding Vectors:**
  - Uses OpenAI embeddings to convert chunks into vector representations.
- **Chroma Vector Store:**
  - Stores vectorized data in separate vector databases for each tab (Academics, Admissions, Professional Development, Information For).

### **4. Unified Knowledge Base**
- Combines vector databases for all tabs into a single unified vector database.
- Enables users to query across all categories in one interface.

### **5. Question-Answering Flow**
- User inputs are processed through a LangChain-powered agent.
- The agent retrieves relevant chunks from the unified vector database using semantic search.
- OpenAI LLM generates responses based on the retrieved information.

---

## **System Workflow**

1. **Scraping Static and Dynamic Data:**
   - Static data is scraped initially and stored with hash values.
   - Dynamic updates are detected by comparing current and previous hash values. Updated pages are re-scraped and stored.

2. **Vector Database Creation:**
   - Process scraped `.txt` or `.pdf` data into chunks.
   - Generate embeddings and store them in Chroma vector databases.

3. **Combining Databases:**
   - Merge individual databases into a unified vector database for all categories.

4. **Question-Answering:**
   - Queries are passed to a LangChain Retrieval Agent.
   - Relevant vectors are retrieved, and OpenAI LLM generates context-aware responses.

---

## **Installation**

### Prerequisites
- Python 3.8 or higher
- [pip](https://pip.pypa.io/en/stable/)

### Clone the Repository
```bash
git clone https://github.com/your-username/pennstate-knowledge-base.git
cd pennstate-knowledge-base
```

### Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

---

## **Configuration**

1. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   ```

2. **Prepare Data Sources:**
   - Add URLs for pages in the Excel file (`data_Updated.xlsx`).
   - Ensure correct tabs for different categories:
     - Sheet1: Academics
     - Sheet2: Admissions
     - Sheet3: Professional Development
     - Sheet4: Information For

---

## **Usage**

### 1. **Scrape and Process Data**
Run the static and dynamic data scripts to scrape and process content:
```bash
python static_academic.py
python dynamic_academic.py
```

### 2. **Create Vector Databases**
Generate vector databases for individual tabs and combine them into a unified database:
```bash
python create_vector_database.py
python combine_vectors.py
```

### 3. **Run the Application**
Launch the Streamlit application:
```bash
streamlit run pennstateapp.py
```

### 4. **Query the Knowledge Base**
- Enter your query in the Streamlit interface.
- The application will retrieve relevant information and display the answer.

---

## **Example Metadata**
| Page_Name            | Link                                                                                     | Hash_Code                                                   |
|----------------------|------------------------------------------------------------------------------------------|------------------------------------------------------------|
| Index Page           | https://greatvalley.psu.edu/                                                            | 7021854581df7f04044cb9daad0d94eedebe4f580ec3d52feaca49e7c7 |
| Academics_Index      | https://greatvalley.psu.edu/academics                                                    | 3365db13b685a64406eb3258d6d420929da05a121822d39b3d4510bd23 |
| Masters_Degree_Index | https://greatvalley.psu.edu/academics/masters-degrees                                    | ca9542b3fb81492746b6e5184471d5747001b780d72ee736ab29fb73b7 |
| AI_Index             | https://greatvalley.psu.edu/academics/masters-degrees/master-artificial-intelligence     | 01fc0ae98a19b71f0471a1c817a657eb9465be46806385ea61159398a6 |
| AI_Schedule          | https://greatvalley.psu.edu/academics/masters-degrees/artificial-intelligence/contact    | 823732d02a9bee85ecf38a1e5c6c5f80a4a989455a8011cb24d8d47e16 |

---

## **Requirements**

### `requirements.txt`
```plaintext
streamlit
openai
langchain
langchain-community
faiss-cpu
python-dotenv
PyPDF2
```

---

## **Future Enhancements**
1. **Automated Update Detection:**
   - Periodically scrape and compare hash values to detect updates automatically.
2. **Expanded Categories:**
   - Add more categories or integrate additional university data.
3. **Deployment:**
   - Deploy the application on cloud platforms for broader accessibility.
4. **Advanced Analytics:**
   - Provide analytics on frequently queried topics or user interaction trends.

---

## **License**
[MIT License](LICENSE)
