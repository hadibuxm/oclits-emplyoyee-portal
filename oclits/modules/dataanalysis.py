from io import BytesIO
import matplotlib.pyplot as plt
import base64
import seaborn as sns
#import seaborn as sns
from . import sheets
#import seaborn as sns 
def task_barchart(userid):
    plt.switch_backend('AGG')
    fetch_data = sheets.fetch_data_for_visualization(userid)
    print(fetch_data)
    tasks = fetch_data[0]
    task_frequency = fetch_data[1]
    fig, axs = plt.subplots(ncols=2)
    sns.barplot(y = tasks, x = task_frequency, ax = axs[0])
    plt.pie(task_frequency, labels = tasks, autopct='%1.2f%%')
    #plt.xlabel("Frequency")
    plt.title(userid)
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_graph():
    # creates memory buffer
    buffer = BytesIO()
    # save image in buffer in png format
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    # get buffer value in string form
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph
