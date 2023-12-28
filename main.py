from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from urllib.parse import quote, unquote

app = FastAPI()
app.add_middleware(CORSMiddleware,
                    allow_origins=['*'],
                    allow_credentials=True,
                    allow_methods=['*'],
                    allow_headers=['*'],
                )

# Configurar credenciales (asegúrate de tener tu archivo credentials.json)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

SAMPLE_SPREADSHEET_ID = '1VRis8EO4Fhtoz5Gcs_71f2i7HUvzKJU5ljX2VU14WgQ'

@app.get("/api/webhook")
async def dude_webhook(
    Time: str = Query(..., title="Time"),
    Device_Name: str = Query(..., title="Device.Name"),
    Device_FirstAddress: Optional[str] = Query(None, title="Device.FirstAddress"),
    Service_Status: Optional[str] = Query(None, title="Service.Status")
):
    try:
          
        '''
        device_name_decoded = unquote(Device_Name) if Device_Name else None
        '''
        # Imprimir la información en la consola
        data = f'Time: {Time}, Device Name: {Device_Name}, Device IP: {Device_FirstAddress}, Status: {Service_Status}'
        print(data)
    
        # Abrir el archivo de Google Sheets y seleccionar una hoja por índice
        spreadsheet = client.open_by_key(SAMPLE_SPREADSHEET_ID)
        worksheet = spreadsheet.get_worksheet(0)

        # Escribir datos en Google Sheets
        worksheet.append_row([Time, Device_Name, Device_FirstAddress, Service_Status])

        # Responder a The Dude para confirmar la recepción de la notificación
        return {"message": "Notificación recibida exitosamente."}
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir durante el procesamiento
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3030)
