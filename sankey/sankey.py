import plotly.graph_objects as go

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 1),
      label = ["Applied: 444", "Rejected: 29", "Coding First Round: 22", 
                "Phone First Round: 33", "Final Round: 10", "Offer: 6", 
                "No Response: 360"]
    ),
    link = dict(
      source = [0, 0, 0, 0, 2, 2, 3, 3, 4, 4], # indices correspond to labels, eg A1, A2, A2, B1, ...
      target = [1, 2, 3, 6, 4, 1, 4, 1, 5, 1],
      value = [29, 22, 33, 360, 14, 2, 2, 31, 6, 4]
  ))])

fig.update_layout(title_text="jobSearch Sankey Diagram", font_size=10)
fig.show()