from zeep import Client
from datetime import datetime
import base64

WORKORDER_NUMBER = "186496"
PDF_FILE_PATH = r"C:\Users\Jeff Goldstein\Documents\Accruent-TMS\TMS test\TMS_Uploader\test.pdf"

WORKORDER_WSDL = "https://fhbio.stage.tmsonline.com/tmsConnect/WorkOrderWS.asmx?wsdl"
DOCUPLOAD_WSDL = "https://fhbio.stage.tmsonline.com/tmsConnect/DocumentUploadWS.asmx?wsdl"

USERNAME = "jgoldstein@pronktech.com"
PASSWORD = "Welcome1!1"
USE_SSO = False

wo_client = Client(WORKORDER_WSDL)

auth_header = wo_client.get_type("ns0:AuthenticationHeader")(
    UserName=USERNAME,
    Password=PASSWORD,
    UseSSOAuthentication=USE_SSO
)

wo_list = wo_client.service.Load(
    header=auth_header,
    workOrderNumber=WORKORDER_NUMBER
)

if not wo_list:
    raise ValueError(f"WorkOrder {WORKORDER_NUMBER} not found")

wo = wo_list[0]

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
existing_completion = getattr(wo, "CompletionComments", "") or ""
new_comment = f"[{timestamp}] Attached Pronk Mobilize App Report"
combined_completion = f"{existing_completion}\n{new_comment}".strip()
setattr(wo, "CompletionComments", combined_completion)

if hasattr(wo, "CustomFields"):
    setattr(wo, "CustomFields", None)

save_result = wo_client.service.Save(
    header=auth_header,
    myWorkOrder=wo
)

doc_client = Client(DOCUPLOAD_WSDL)

with open(PDF_FILE_PATH, "rb") as f:
    file_bytes = f.read()

file_b64 = base64.b64encode(file_bytes).decode("utf-8")

WORK_ORDER_ID = wo.WorkOrderID
SEGMENT_ID = 4

document_upload = {
    "SegmentID": SEGMENT_ID,
    "ModuleId": "WORK_ORDERS",
    "ItemID": WORK_ORDER_ID,
    "KeyID": WORK_ORDER_ID,
    "FieldId": 0,
    "StatusCode": "ACTIV",
    "TypeCode": "FL",
    "Description": "Manual Preventative Maintenance",
    "Value": "test.pdf",
    "ValidateForDataImport": False,
    "DocumentUploadID": 0
}

header_type = doc_client.get_type("ns0:AuthenticationHeader")
doc_header = header_type(
    UserName=USERNAME,
    Password=PASSWORD,
    UseSSOAuthentication=USE_SSO
)

response = doc_client.service.SaveFile(
    header=doc_header,
    documentUpload=document_upload,
    document=file_b64
)

print("WorkOrder updated and document uploaded successfully.")
print(response)
