import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox, simpledialog

# Initialize an undirected graph for the social network
social_network = nx.Graph()
last_mutual_friends = []  # To highlight in visualization

# Function to add a user to the network
def add_user():
    user = simpledialog.askstring("Input", "Enter the user's name:")
    if user:
        if user not in social_network:
            social_network.add_node(user)
            messagebox.showinfo("Success", f"User '{user}' added to the network.")
        else:
            messagebox.showerror("Error", f"User '{user}' already exists in the network.")

# Function to add a friendship between two users
def add_friendship():
    user1 = simpledialog.askstring("Input", "Enter the first user's name:")
    user2 = simpledialog.askstring("Input", "Enter the second user's name:")
    
    if user1 and user2:
        if user1 in social_network and user2 in social_network:
            social_network.add_edge(user1, user2)
            messagebox.showinfo("Success", f"Friendship created between '{user1}' and '{user2}'.")
        else:
            messagebox.showerror("Error", "Both users must exist in the network before adding a friendship.")

# Function to find mutual friends between two users
def find_mutual_friends():
    global last_mutual_friends
    user1 = simpledialog.askstring("Input", "Enter the first user's name:")
    user2 = simpledialog.askstring("Input", "Enter the second user's name:")
    
    if user1 and user2:
        if social_network.has_node(user1) and social_network.has_node(user2):
            last_mutual_friends = list(nx.common_neighbors(social_network, user1, user2))
            messagebox.showinfo("Mutual Friends", f"Mutual friends between '{user1}' and '{user2}': {last_mutual_friends}")
        else:
            messagebox.showerror("Error", "One or both users do not exist in the network.")

# Function to suggest friends for a user
def suggest_friends():
    user = simpledialog.askstring("Input", "Enter the user's name for friend suggestions:")
    
    if user:
        if social_network.has_node(user):
            suggestions = set()
            for friend in social_network.neighbors(user):
                for friend_of_friend in social_network.neighbors(friend):
                    if friend_of_friend != user and friend_of_friend not in social_network.neighbors(user):
                        suggestions.add(friend_of_friend)
            messagebox.showinfo("Friend Suggestions", f"Friend suggestions for '{user}': {suggestions}")
        else:
            messagebox.showerror("Error", f"User '{user}' does not exist in the network.")


# Function to find the shortest path between two users
# def find_shortest_path():
#     user1 = simpledialog.askstring("Input", "Enter the first user's name:")
#     user2 = simpledialog.askstring("Input", "Enter the second user's name:")
    
#     if user1 and user2:
#         if social_network.has_node(user1) and social_network.has_node(user2):
#             try:
#                 path = nx.shortest_path(social_network, source=user1, target=user2)
#                 messagebox.showinfo("Shortest Path", f"Connection between '{user1}' and '{user2}': {path}")
#             except nx.NetworkXNoPath:
#                 messagebox.showinfo("Shortest Path", f"No connection between '{user1}' and '{user2}'.")
#         else:
#             messagebox.showerror("Error", "One or both users do not exist in the network.")


# Function to remove a user
def remove_user():
    user = simpledialog.askstring("Input", "Enter the user's name to remove:")
    if user in social_network:
        social_network.remove_node(user)
        messagebox.showinfo("Removed", f"User '{user}' removed from the network.")
    else:
        messagebox.showerror("Error", "User not found.")

# Function to remove a friendship
def remove_friendship():
    user1 = simpledialog.askstring("Input", "Enter the first user's name:")
    user2 = simpledialog.askstring("Input", "Enter the second user's name:")
    if social_network.has_edge(user1, user2):
        social_network.remove_edge(user1, user2)
        messagebox.showinfo("Removed", f"Friendship between '{user1}' and '{user2}' removed.")
    else:
        messagebox.showerror("Error", "Friendship not found.")

# Function to detect communities
def detect_communities():
    communities = list(nx.connected_components(social_network))
    result = ""
    for i, community in enumerate(communities):
        result += f"Community {i+1}: {list(community)}\n"
    messagebox.showinfo("Communities", result)

# Function to save the network
def save_network():
    nx.write_gml(social_network, "social_network.gml")
    messagebox.showinfo("Saved", "Network saved to 'social_network.gml'.")

# Function to load the network
def load_network():
    global social_network
    try:
        social_network = nx.read_gml("social_network.gml")
        messagebox.showinfo("Loaded", "Network loaded from 'social_network.gml'.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Save file not found.")

# Function to visualize the social network graph
def visualize_network():
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(social_network, seed=42)
    node_colors = ['green' if node in last_mutual_friends else 'red' for node in social_network.nodes()]
    nx.draw(social_network, pos, with_labels=True, node_color=node_colors, edge_color='black', node_size=2000, font_size=10)
    plt.title("Social Network Graph\n(Green = Mutual Friends)")
    plt.show()

# Function to display the main app menu
def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    Button(root, background="lightblue", text="Add User", command=add_user, width=25).pack(pady=5)
    Button(root, background="lightblue", text="Add Friendship", command=add_friendship, width=25).pack(pady=5)
    Button(root, background="lightblue", text="Find Mutual Friends", command=find_mutual_friends, width=25).pack(pady=5)
    Button(root, background="lightblue", text="Suggest Friends", command=suggest_friends, width=25).pack(pady=5)
    # Button(root, background="lightblue", text="Shortest Path", command=find_shortest_path, width=25).pack(pady=5)
    Button(root, background="lightblue", text="Remove User", command=remove_user, width=25).pack(pady=5)
    Button(root, background="lightblue", text="Remove Friendship", command=remove_friendship, width=25).pack(pady=5)
    Button(root, background="lightblue", text="Detect Communities", command=detect_communities, width=25).pack(pady=5)
    Button(root, background="lightblue", text="Save Network", command=save_network, width=25).pack(pady=5)
    Button(root, background="lightblue", text="Load Network", command=load_network, width=25).pack(pady=5)
    Button(root, background="lightblue", text="Visualize Network", command=visualize_network, width=25).pack(pady=5)
    Button(root, background="lightblue", text="Exit", command=root.quit, width=25).pack(pady=5)

# Function to display group details
def display_group_details():
    frame = Frame(root, bg="white", bd=5, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=200)

    label = Label(
        frame, 
        text=(
            "Group Details:\n\n"
            "Student Name: Ashutosh Sarin\n"
            "UID: 24MCI10022\n\n"
            "Student Name: Bhanu Saini\n"
            "UID: 24MCI10026\n\n"
            "Section/Group: 24MAM1-A\n"
            "Subject: Artificial Intelligence\n"
            "Project Title: Social Network Graph App"
        ),
        font=("Bookman Old Style", 10, "bold"),
        bg="white",
        justify="center"
    )
    label.pack(expand=True)
    
    root.after(5500, show_main_menu)

# Main GUI window
root = Tk()
root.title("Social Network Graph Analysis")
root.geometry("400x600")
root.config(bg="black")

# Display the group details screen on startup
display_group_details()

# Event loop
root.mainloop()