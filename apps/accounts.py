import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

import create_plot
import utils
import init_database

df = init_database.init_database()

layout = html.Div([
    html.Div([
        html.H2("Wallets"),
        # Cash
        html.Div([
            # image
            html.Div([
                html.Img(
                    src="/assets/100K_cash.jpeg",
                    height=30
                )
            ], style={'display':'inline-block',
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "5px 5px 5px 5px",
                        "height": "30px"}),
            
            # amount
            html.Div([
                html.P(f"VND {utils.money_in_cash(df):,}")
            ], style={'display':'inline-block', 
                        "height": "30px", 
                        "text-align": "center",
                        "float":"right",
                        }),
            
            html.Hr(
                className="dashed"
            ),
            
            html.Div([
                html.H5("Cash")
            ]),
            
        ], style={"width":"200px",
                    "height":"80px",
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)", 
                    "border-radius": "5px",
                    "padding": "20px 20px",
                    'display':'inline-block',
                    "margin-right": "20px",
                    "margin-bottom": "20px"
                    }),
        
        # Home savings
        html.Div([
            # image
            html.Div([
                html.Img(
                    src="/assets/100K_cash.jpeg",
                    height=30
                )
            ], style={'display':'inline-block',
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "5px 5px 5px 5px",
                        "height": "30px"}),
            
            # amount
            html.Div([
                html.P(f"VND {utils.money_in_home(df):,}")
            ], style={'display':'inline-block', 
                        "height": "30px", 
                        "text-align": "center",
                        "float":"right",
                        }),
            
            html.Hr(
                className="dashed"
            ),
            
            html.Div([
                html.H5("Cash at Home")
            ]),
            
        ], style={"width":"200px",
                    "height":"80px",
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)", 
                    "border-radius": "5px",
                    "padding": "20px 20px",
                    'display':'inline-block',
                    "margin-right": "20px",
                    "margin-bottom": "20px"
                    }),
        

        html.Hr(className="dashed")
    ]),

    html.Div([
        html.H2("eWallets"),
        
        # MOCA
        html.Div([
            # image
            html.Div([
                html.Img(
                    src="/assets/moca.jpeg",
                    height=30
                )
            ], style={'display':'inline-block',
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "5px 5px 5px 5px",
                        "height": "30px"}),
            
            # amount
            html.Div([
                html.P(f"VND {utils.money_in_moca(df):,}")
            ], style={'display':'inline-block', 
                        "height": "30px", 
                        "text-align": "center",
                        "float":"right",
                        }),
            
            html.Hr(
                className="dashed"
            ),
            
            html.Div([
                html.H5("MOCA")
            ]),
            
        ], style={"width":"200px",
                    "height":"80px",
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)", 
                    "border-radius": "5px",
                    "padding": "20px 20px",
                    'display':'inline-block',
                    "margin-right": "20px",
                    "margin-bottom": "20px"
                    }),
        
        html.Hr(className="dashed")
    ]),

    html.Div([
        html.H2("Plastic Cards"),
        
        # ACB
        html.Div([
            # image
            html.Div([
                html.Img(
                    src="/assets/acb_card.png",
                    height=30
                )
            ], style={'display':'inline-block',
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "5px 5px 5px 5px",
                        "height": "30px"}),
            
            # amount
            html.Div([
                html.P(f"VND {utils.money_in_acb_card(df):,}")
            ], style={'display':'inline-block', 
                        "height": "30px", 
                        "text-align": "center",
                        "float":"right",
                        }),
            
            html.Hr(
                className="dashed"
            ),
            
            html.Div([
                html.H5("Fulbright ACB")
            ]),
            
        ], style={"width":"200px",
                    "height":"80px",
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)", 
                    "border-radius": "5px",
                    "padding": "20px 20px",
                    'display':'inline-block',
                    "margin-right": "20px",
                    "margin-bottom": "20px"
                    }),
        
        # VCB VISA
        html.Div([
            # image
            html.Div([
                html.Img(
                    src="/assets/visa_card.jpeg",
                    height=30
                )
            ], style={'display':'inline-block',
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "5px 5px 5px 5px",
                        "height": "30px"}),
            
            # amount
            html.Div([
                html.P(f"VND {utils.money_in_visa_card(df):,}")
            ], style={'display':'inline-block', 
                        "height": "30px", 
                        "text-align": "center",
                        "float":"right",
                        }),
            
            html.Hr(
                className="dashed"
            ),
            
            html.Div([
                html.H5("VISA Card")
            ]),
            
        ], style={"width":"200px",
                    "height":"80px",
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)", 
                    "border-radius": "5px",
                    "padding": "20px 20px",
                    'display':'inline-block',
                    "margin-right": "20px",
                    "margin-bottom": "20px"
                    }),

        html.Hr(className="dashed")
    ]), 


    html.Div([
        html.H2("Savings"),
        
        # Finhay Profit
        html.Div([
            # image
            html.Div([
                html.Img(
                    src="/assets/finhay.png",
                    height=30
                )
            ], style={'display':'inline-block',
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "5px 5px 5px 5px",
                        "height": "30px",
                        "margin-right": "20px"
                        }),
            
            # amount
            html.Div([
                html.P(f"VND {utils.money_in_finhay(df):,}")
            ], style={'display':'inline-block', 
                        "height": "30px", 
                        "text-align": "center",
                        "float":"right",
                        }),
            
            html.Hr(
                className="dashed"
            ),
            
            html.Div([
                html.H5("Finhay Profits")
            ]),
            
        ], style={"width":"200px",
                    "height":"80px",
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)", 
                    "border-radius": "5px",
                    "padding": "20px 20px",
                    'display':'inline-block',
                    "margin-right": "20px",
                    "margin-bottom": "20px"
                    }),
        
        # 3-month savings
        html.Div([
            # image
            html.Div([
                html.Img(
                    src="/assets/finhay.png",
                    height=30
                )
            ], style={'display':'inline-block',
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "5px 5px 5px 5px",
                        "height": "30px"}),
            
            # amount
            html.Div([
                html.P(f"VND {utils.money_in_finhay(df):,}")
            ], style={'display':'inline-block', 
                        "height": "30px", 
                        "text-align": "center",
                        "float":"right",
                        }),
            
            html.Hr(
                className="dashed"
            ),
            
            html.Div([
                html.H5("3-Month Savings")
            ]),
            
        ], style={"width":"200px",
                    "height":"80px",
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)", 
                    "border-radius": "5px",
                    "padding": "20px 20px",
                    'display':'inline-block',
                    "margin-right": "20px",
                    "margin-bottom": "20px"
                    }),
        
        # Finhay Gold
        html.Div([
            # image
            html.Div([
                html.Img(
                    src="/assets/finhay.png",
                    height=30
                )
            ], style={'display':'inline-block',
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "5px 5px 5px 5px",
                        "height": "30px"}),
            
            # amount
            html.Div([
                html.P(f"VND {utils.money_in_finhay(df):,}")
            ], style={'display':'inline-block', 
                        "height": "30px", 
                        "text-align": "center",
                        "float":"right",
                        }),
            
            html.Hr(
                className="dashed"
            ),
            
            html.Div([
                html.H5("Gold")
            ]),
            
        ], style={"width":"200px",
                    "height":"80px",
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)", 
                    "border-radius": "5px",
                    "padding": "20px 20px",
                    'display':'inline-block',
                    "margin-right": "20px",
                    "margin-bottom": "20px"
                    }),
        
        # Macbook savings
        html.Div([
            # image
            html.Div([
                html.Img(
                    src="/assets/finhay.png",
                    height=30
                )
            ], style={'display':'inline-block',
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "5px 5px 5px 5px",
                        "height": "30px"}),
            
            # amount
            html.Div([
                html.P(f"VND {utils.money_in_finhay(df):,}")
            ], style={'display':'inline-block', 
                        "height": "30px", 
                        "text-align": "center",
                        "float":"right",
                        }),
            
            html.Hr(
                className="dashed"
            ),
            
            html.Div([
                html.H5("Macbook")
            ]),
            
        ], style={"width":"200px",
                    "height":"130px",
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)", 
                    "border-radius": "5px",
                    "padding": "20px 20px",
                    'display':'inline-block',
                    "margin-right": "20px",
                    "margin-bottom": "20px"
                    }),
        
        # Emergency savings
        html.Div([
            # image
            html.Div([
                html.Img(
                    src="/assets/finhay.png",
                    height=30
                )
            ], style={'display':'inline-block',
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "5px 5px 5px 5px",
                        "height": "30px"}),
            
            # amount
            html.Div([
                html.P(f"VND {utils.money_in_finhay(df):,}")
            ], style={'display':'inline-block', 
                        "height": "30px", 
                        "text-align": "center",
                        "float":"right",
                        }),
            
            html.Hr(
                className="dashed"
            ),
            
            html.Div([
                html.H5("Emergency")
            ]),
            
        ], style={"width":"200px",
                    "height":"80px",
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)", 
                    "border-radius": "5px",
                    "padding": "20px 20px",
                    'display':'inline-block',
                    "margin-right": "20px",
                    "margin-bottom": "20px"
                    }),
        
        # Donation savings
        html.Div([
            # image
            html.Div([
                html.Img(
                    src="/assets/finhay.png",
                    height=30
                )
            ], style={'display':'inline-block',
                        "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)",
                        "border-radius": "5px 5px 5px 5px",
                        "height": "30px"}),
            
            # amount
            html.Div([
                html.P(f"VND {utils.money_in_finhay(df):,}")
            ], style={'display':'inline-block', 
                        "height": "30px", 
                        "text-align": "center",
                        "float":"right",
                        }),
            
            html.Hr(
                className="dashed"
            ),
            
            html.Div([
                html.H5("Donation")
            ]),
            
        ], style={"width":"200px",
                    "height":"80px",
                    "box-shadow": "0 4px 8px 0 rgba(0,0,0,0.2)", 
                    "border-radius": "5px",
                    "padding": "20px 20px",
                    'display':'inline-block',
                    "margin-right": "20px",
                    "margin-bottom": "20px"
                    }),
        
        html.Hr(className="dashed")
    ])
])