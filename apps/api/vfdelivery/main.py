from fastapi import FastAPI

app = FastAPI(
    title='VFDelivery',
    description='Aplicação de food delivery focada no fluxo de pedidos e avaliações.'
)


@app.get('')
def root():
    return {'status': 'OK'}
