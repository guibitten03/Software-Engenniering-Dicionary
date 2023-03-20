from app import *

nav_block_style = {
    "margin-bottom":"1em"
}

## DATASETS
data = pd.read_csv("definitions.csv")

add_modal = dbc.Modal([
        dbc.ModalHeader("Adicionar Definição:"),
        dbc.ModalBody([
            dbc.Input(id="add-modal-term", placeholder="Digite o termo", type='text'),
            dbc.Input(id="add-modal-def", placeholder="Digite a definição", type='text'),
            dbc.Button("Adicionar" ,id="add-def-csv", color="success",
                       className="me-1")
        ])
], id="add-modal", is_open=False)


ex_modal = dbc.Modal([
        dbc.ModalHeader("Excluir Definição:"),
        dbc.ModalBody([
            dbc.Input(id="ex-modal-term", placeholder="Digite o termo", type='text'),
            dbc.Button("Excluir" ,id="ex-def-csv", color="danger",
                       className="me-1")
        ])
], id="ex-modal", is_open=False)

app.layout = dbc.Row([  # Main Container
    
    add_modal,
    ex_modal,
    
    dcc.Store(id="database", data=data.to_dict()),

    dbc.Col([

        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H3("Dicionário de Engenharia de Software")
                    ])
                ], style=nav_block_style),

                dbc.Row([
                    dbc.Col([
                        dbc.Button("Adicionar", color="success",
                                   className="me-1", id="add-definition")
                    ])
                ], style=nav_block_style),

                dbc.Row([
                    dbc.Col([
                        dbc.Button("Excluir", color="danger",
                                   className="me-1", id="ex-definition")
                    ])
                ], style=nav_block_style)
            ])
        ], className="h-75")

    ], md=2),

    dbc.Col([
        
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Input(id="search-input", placeholder="Busque pela palavra...", type="text")
                    ], md = 10),
                    dbc.Col([
                        dbc.Button("Pesquisar", color="primary",
                                   className="me-1", id="search-term")
                    ], md = 2)
                ])
            ])
        ], style=nav_block_style),

        dbc.Row([
            dbc.Col([
                dbc.Accordion(id = "definition-container")
            ], md = 10)
        ])

    ], md=10)
], className="p-5 vh-100")


@app.callback(
    Output("definition-container", "children"),
    Input("search-term", "n_clicks"),
    State("search-input", "value"),
    State("database", "data")
)
def charge_search(n, search, df):

    df = pd.DataFrame(df)
    definitions = []

    if search == None:

        if df.shape[0] != 0:
            for i in range(df.shape[0]):
                comp = dbc.AccordionItem([
                    html.P(f"{df.iloc[i, 1]}")
                ], title=f"{df.iloc[i, 0]}")
                definitions.append(comp)

    else:
        df = df.loc[df['term'].str.contains(search)]
        if df.shape[0] != 0:
            for i in range(df.shape[0]):
                comp = dbc.AccordionItem([
                    html.P(f"{df.iloc[i, 1]}")
                ], title=f"{df.iloc[i, 0]}")
                definitions.append(comp)
        else:
            definitions.append(dbc.AccordionItem([
                html.P("Não foi possível encontrar este item.")
            ], title="Item não encontrado."))


    return definitions


@app.callback(
    Output("add-modal", "is_open"),
    Input("add-definition", "n_clicks"),
    State("add-modal", "is_open")
)
def toggle_add_modal(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("ex-modal", "is_open"),
    Input("ex-definition", "n_clicks"),
    State("ex-modal", "is_open")
)
def toggle_ex_modal(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("database", "data"),
    Input("add-def-csv", "n_clicks"),
    [State("add-modal-term", "value"),
     State("add-modal-def", "value")]
)
def add_definition_in_csv(n, term, defi):
    data = pd.read_csv("definitions.csv")

    if n != 0:
        if term != None:
            if defi != None:
                
                import pdb
                pdb.set_trace()

                data.loc[len(data)] = [term, defi]

                data.to_csv("definitions.csv", index=False)
                return data.to_dict()


if __name__ == "__main__":
    app.run_server(debug=True)
