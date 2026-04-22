# Modified app.py - Using HTMLResponse instead of Jinja2 templates
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from uvicorn import run as app_run
import os
from typing import Optional

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Static files
static_dir = os.path.join(BASE_DIR, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Read HTML template as string
html_template_path = os.path.join(BASE_DIR, "templates", "vehicledata.html")
with open(html_template_path, 'r', encoding='utf-8') as f:
    HTML_TEMPLATE = f.read()

class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.Gender: Optional[int] = None
        self.Age: Optional[int] = None
        self.Driving_License: Optional[int] = None
        self.Region_Code: Optional[float] = None
        self.Previously_Insured: Optional[int] = None
        self.Annual_Premium: Optional[float] = None
        self.Policy_Sales_Channel: Optional[float] = None
        self.Vintage: Optional[int] = None
        self.Vehicle_Age_lt_1_Year: Optional[int] = None
        self.Vehicle_Age_gt_2_Years: Optional[int] = None
        self.Vehicle_Damage_Yes: Optional[int] = None

    async def get_vehicle_data(self):
        form = await self.request.form()
        self.Gender = form.get("Gender")
        self.Age = form.get("Age")
        self.Driving_License = form.get("Driving_License")
        self.Region_Code = form.get("Region_Code")
        self.Previously_Insured = form.get("Previously_Insured")
        self.Annual_Premium = form.get("Annual_Premium")
        self.Policy_Sales_Channel = form.get("Policy_Sales_Channel")
        self.Vintage = form.get("Vintage")
        self.Vehicle_Age_lt_1_Year = form.get("Vehicle_Age_lt_1_Year")
        self.Vehicle_Age_gt_2_Years = form.get("Vehicle_Age_gt_2_Years")
        self.Vehicle_Damage_Yes = form.get("Vehicle_Damage_Yes")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Remove Jinja2 placeholders for GET request
    html = HTML_TEMPLATE.replace("{% if context %}", "")
    html = html.replace("{% endif %}", "")
    html = html.replace("{{ context }}", "Ready for prediction")
    return html

@app.get("/train")
async def trainRouteClient():
    try:
        from src.pipline.training_pipeline import TrainPipeline
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful!!!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.post("/", response_class=HTMLResponse)
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        await form.get_vehicle_data()
        
        from src.pipline.prediction_pipeline import VehicleData, VehicleDataClassifier
        
        vehicle_data = VehicleData(
            Gender=form.Gender, Age=form.Age,
            Driving_License=form.Driving_License, Region_Code=form.Region_Code,
            Previously_Insured=form.Previously_Insured, Annual_Premium=form.Annual_Premium,
            Policy_Sales_Channel=form.Policy_Sales_Channel, Vintage=form.Vintage,
            Vehicle_Age_lt_1_Year=form.Vehicle_Age_lt_1_Year,
            Vehicle_Age_gt_2_Years=form.Vehicle_Age_gt_2_Years,
            Vehicle_Damage_Yes=form.Vehicle_Damage_Yes
        )

        vehicle_df = vehicle_data.get_vehicle_input_data_frame()
        model_predictor = VehicleDataClassifier()
        value = model_predictor.predict(dataframe=vehicle_df)[0]
        status = "Response-Yes" if value == 1 else "Response-No"

        # Manually replace the placeholder in HTML
        html = HTML_TEMPLATE
        if "{% if context %}" in html:
            # Simple replacement for the result section
            result_html = f'<div class="result"><h2>Result: {status}</h2></div>'
            html = html.replace('{% if context %}\n            <div class="result">\n                <h2>Result: {{ context }}</h2>\n            </div>\n        {% endif %}', result_html)
        else:
            # Fallback: simple replace
            html = html.replace("{{ context }}", status)
        
        return html
        
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error: {e}</h1>", status_code=500)

if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=5000)