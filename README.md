# SciLifeLab Workshop: AI Agents in Life Sciences

Presentation:
- [Section 1](https://1drv.ms/p/c/edc89288e35ae05d/EUIjZr76uqJOnr3y6P5ne6oBkhO95rPaLm68aHsvmyCVew)


# Setup Before the Workshop

Make sure your environment is ready before you begin:

## 1. Open a terminal and clone Github repo: 
```bash
git clone https://github.com/DinhLongHuynh/SciLifeLab_agent_workshop
```

## 2. Navigate to the project directory:
```bash
cd SciLifeLab_agent_workshop
```

## 3. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
 ```
    
## 4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## 5. Register your virtual environment as a Jupyter kernel:

```bash
python -m ipykernel install --user --name=SciLifeLab_venv --display-name="SciLifeLab_workshop_kernel"
```

## 6. Start Jupyter notebook:
```bash
jupyter notebook
```

## 7. You can find the notebooks in the following directories:

`SciLifeLab_agent_workshop/Section_1_LangGraph/`

`SciLifeLab_agent_workshop/Section_2_MCP/MCP_scratch/`

## 8. From the top-right corner of the Jupyter notebook, select and change the kernel:

**Example:** `SciLifeLab_agent_workshop/Section_1_LangGraph/langgraph_lab.ipynb`

click `Python 3 (ipykernel)` → select `Select kernel for: "langgraph_lab.ipynb"` → from the drop-down menu, choose `SciLifeLab_workshop_kernel` → check `Always start the preferred kernel` → click `Select`

---

You can now start exploring and using the notebooks

Happy learning! 😊
