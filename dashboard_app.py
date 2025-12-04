from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.graph_objects as go
import pandas as pd

def create_app(data_handler):
    """
    Creates and configures the Dash application.
    """
    app = Dash(__name__)

    # Get initial summary data
    summary = data_handler.get_category_summary()
    
    # Get column names from handler
    real_amount_col = data_handler.amount_col
    real_business_col = data_handler.business_col

    # Create the Pie Chart
    fig = go.Figure(data=[go.Pie(
        labels=summary.index,
        values=summary.values,
        hole=0.3, # Donut style
        textinfo='label+percent',
        textposition='inside',
        hoverinfo='label+value+percent',
        customdata=summary.index # Pass label explicitly for click data
    )])
    
    fig.update_layout(
        title_text='סכום עסקאות לפי ענף (לחץ על פלח לפירוט)',
        title_x=0.5,
        clickmode='event+select',
        showlegend=False,
        height=800
    )

    # Define Safe Column IDs for the Table (avoids Hebrew/Encoding issues in CSS)
    # Ordering: Amount first (Left), Business second (Right) to simulate RTL in LTR mode
    TABLE_COLUMNS = []
    if real_amount_col:
        TABLE_COLUMNS.append({'name': 'סכום חיוב', 'id': 'amount_col'})
    if real_business_col:
        TABLE_COLUMNS.append({'name': 'שם בית העסק', 'id': 'business_col'})

    # Calculate total expenses
    total_expenses = 0
    if data_handler.amount_col and not data_handler.df.empty:
         total_expenses = data_handler.df[data_handler.amount_col].sum()

    # --- Comparison Bar Chart Logic ---
    avg_summary, avg_total = data_handler.get_comparison_stats()

    # Combine categories
    all_categories = sorted(list(set(summary.index) | set(avg_summary.index)))
    
    # Prepare values
    current_values = [summary.get(cat, 0) for cat in all_categories]
    avg_values = [avg_summary.get(cat, 0) for cat in all_categories]
    
    # Add Total
    all_categories = ['סה"כ'] + all_categories
    current_values = [total_expenses] + current_values
    avg_values = [avg_total] + avg_values
    
    bar_fig = go.Figure(data=[
        go.Bar(name='נוכחי', x=all_categories, y=current_values, text=current_values, texttemplate='%{text:.0f}', textposition='auto'),
        go.Bar(name='ממוצע', x=all_categories, y=avg_values, text=avg_values, texttemplate='%{text:.0f}', textposition='auto')
    ])
    
    bar_fig.update_layout(
        title_text='השוואה לממוצע חודשי (נוכחי מול ממוצע חודשים קודמים)',
        title_x=0.5,
        barmode='group',
        xaxis_title='קטגוריה',
        yaxis_title='סכום (₪)',
        height=500
    )
    # ----------------------------------

    # Define the App Layout
    # Removed global RTL to avoid Table layout issues
    app.layout = html.Div([
        # Header
        html.H1(f"דוח הוצאות - {data_handler.filename}", style={'textAlign': 'center', 'fontFamily': 'Arial', 'direction': 'rtl'}),
        html.H2(f"סה\"כ לחודש: {total_expenses:,.2f} ₪", style={'textAlign': 'center', 'fontFamily': 'Arial', 'direction': 'rtl', 'color': '#2c3e50'}),
        
        # Main Container
        html.Div([
            # Left Side: Pie Chart
            html.Div([
                dcc.Graph(id='category-pie-chart', figure=fig)
            ], style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            
            # Right Side: Detail Table
            html.Div([
                html.H3(id='table-title', children='פירוט עסקאות', style={'textAlign': 'center', 'direction': 'rtl'}),
                dash_table.DataTable(
                    id='details-table',
                    columns=TABLE_COLUMNS,
                    data=[],
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'right', 
                        'fontFamily': 'Arial',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'padding': '10px'
                    },
                    # simplified width control using safe IDs
                    style_cell_conditional=[
                        {
                            'if': {'column_id': 'business_col'},
                            'width': '70%' 
                        },
                        {
                            'if': {'column_id': 'amount_col'},
                            'width': '30%'
                        }
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',
                        'textAlign': 'right'
                    }
                )
            ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': '20px'})
        ]),
        
        # Comparison Chart Section
        html.Div([
            html.Hr(),
            dcc.Graph(id='comparison-bar-chart', figure=bar_fig)
        ], style={'width': '95%', 'margin': 'auto', 'marginTop': '30px'})
    ])

    # Define Interaction Callback
    @app.callback(
        [Output('details-table', 'data'),
         Output('table-title', 'children')],
        [Input('category-pie-chart', 'clickData')]
    )
    def update_table(clickData):
        if clickData is None:
            return [], "לחץ על פלח בגרף להצגת נתונים"

        # Extract category name from the clicked point
        category_name = clickData['points'][0]['label']
        
        # Get detailed data
        details_df = data_handler.get_details_by_category(category_name)
        
        # Calculate total
        total_val = 0
        if real_amount_col and real_amount_col in details_df.columns:
            total_val = details_df[real_amount_col].sum()
        
        # Transform data to match our safe IDs
        safe_data = []
        for _, row in details_df.iterrows():
            item = {}
            if real_business_col and real_business_col in row:
                item['business_col'] = row[real_business_col]
            if real_amount_col and real_amount_col in row:
                item['amount_col'] = row[real_amount_col]
            safe_data.append(item)
        
        # Add summary row
        summary_row = {}
        if 'business_col' in [col['id'] for col in TABLE_COLUMNS]: # If business col exists
             summary_row['business_col'] = 'סה"כ'
        
        if real_amount_col:
             summary_row['amount_col'] = round(total_val, 2)
        
        safe_data.append(summary_row)
        
        return safe_data, f"פירוט עבור: {category_name}"

    return app
