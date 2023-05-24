from app import *

nav_block_style = {
    "margin-bottom":"2em"
}

last_btn_trigget = 0

def define_pag_nums():
    data = pd.read_csv("data/definitions.csv")
    
    page_size = 12
    
    num_pages = math.ceil(data.shape[0] / page_size)
    
    return num_pages


## DATASETS
data = pd.read_csv("data/definitions.csv")


add_modal = dbc.Modal([
        dbc.ModalHeader("Adicionar Definição:"),
        dbc.ModalBody([
            dbc.Input(id="add-modal-term", placeholder="Digite o termo", type='text', style=nav_block_style),
            dbc.Textarea(
                valid=True,
                className="mb-3",
                placeholder="Digite a definição...",
                id="add-modal-def"
            ),
            dbc.Button("Adicionar" ,id="add-def-csv", color="success",
                       className="me-1", style=nav_block_style),
            html.Div(id = "add-suc")
        ])
], id="add-modal", is_open=False)


ex_modal = dbc.Modal([
        dbc.ModalHeader("Excluir Definição:"),
        dbc.ModalBody([
            dbc.Input(id="ex-modal-term", placeholder="Digite o termo", type='text', style=nav_block_style),
            dbc.Button("Excluir" ,id="ex-def-csv", color="danger",
                       className="me-1", style=nav_block_style),
            html.Div(id = "ex-suc")
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
                        html.H3("Dicionário de Engenharia de Software",
                                style={
                                    "color":"white",
                                    "font-weight":"bold"
                                    }
                                )
                    ])
                ], style=nav_block_style),

                dbc.Row([
                    dbc.Col([
                        dbc.Button("Adicionar", className="me-1",
                                   id="add-definition", style={
                                       "background-color":"#03C988",
                                       "width":"90%"
                                   })
                    ], className="d-flex justify-content-center")
                ], style=nav_block_style),

                dbc.Row([
                    dbc.Col([
                        dbc.Button("Excluir", color="danger",
                                   className="me-1", id="ex-definition",
                                   style={
                                       "width":"90%"
                                   })
                    ],className="d-flex justify-content-center")
                ], style=nav_block_style),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Listar Palavras", className="me-1",
                                   id="list-words", style={
                                       "width":"90%",
                                       "background-color":"#1C82AD"
                                   })
                    ],className="d-flex justify-content-center")
                ], style=nav_block_style),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Listar Definições", className="me-1",
                                   id="list-definitions", style={
                                       "width":"90%",
                                       "background-color":"#1C82AD"
                                   })
                    ],className="d-flex justify-content-center")
                ], style=nav_block_style)
            ])
        ], className="h-75", style={"background-color":"#00337C"})

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
                dbc.Pagination(
                id="pag_container",
                max_value=define_pag_nums()
            )
            ], id="pagination"),
        ], style={"height":"3em"}),

        dbc.Row([
            dbc.Col([
                
            ], md = 10, id = "definition-container")
        ]),

        
    ], md=10)
], className="p-5 vh-100", style={"background-color":"#13005A"})

    

@app.callback(
    Output("definition-container", "children"),
    [
        Input("search-term", "n_clicks"),
        Input("list-words", "n_clicks"),
        Input("list-definitions", "n_clicks"),
        Input("pag_container", "active_page")
    ],
    [
        State("search-input", "value"),
    ]
)
def charge_search(n, wor, defi, pag, search):
    
    if ctx.triggered_id == "list-definitions": search = None
    
    if pag == None: pag = 1
    
    df = pd.read_csv("data/definitions.csv")
    
    pag_range = {
        1: [0,11],
        2: [12,23],
        3: [24,35],
        4: [36,47],
        5: [48,59]
    }
    
    definitions = []
    
    
    if ctx.triggered_id == "list-words":
        list_group = []
        if df.shape[0] != 0:
            for term in range(df['term'].shape[0]):
                list_group.append(dbc.ListGroupItem(df['term'][term]))
                    
        else:
            list_group.append("Nenhum Termo Registrado")
        
        return dbc.ListGroup(list_group)
        
    else:
        if search == None:

            if df.shape[0] != 0:
                for i in range(pag_range[pag][0],pag_range[pag][1]):
                    if i < df.shape[0]:
                        comp = dbc.AccordionItem([
                            html.P(f"{df.iloc[i, 1]}")
                        ], title=f"{df.iloc[i, 0]}")
                        definitions.append(comp)

        else:
            
            df = df.loc[df['term'] == search]
            
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


        return dbc.Accordion(definitions)


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
    data = pd.read_csv("data/definitions.csv")

    if n != 0:
        if term != None:
            if defi != None:

                data.loc[len(data)] = [term, defi]

                data.to_csv("data/definitions.csv", index=False)
                return data.to_dict()
            
    else:
        return data.to_dict()

@app.callback(
    Output("ex-suc", "children"),
    Input("ex-def-csv", "n_clicks"),
    State("ex-modal-term", "value")
)
def ex_term_in_csv(n, term):
    data = pd.read_csv("data/definitions.csv")
    
    if n != 0:
        if term != None:
            if data.loc[data['term'] == term].shape[0] != 0:
                    data = data.loc[data['term'] != term]
                    data.to_csv("data/definitions.csv", index=None)
                    
                    return dbc.Alert("Removed Successfull!", color="success")
                
    else:
        return dbc.Alert("Could not remove this term.", color="danger")
        


if __name__ == "__main__":
    app.run_server(debug=True)
