from matplotlib import pyplot as plt
from collections import Counter
import re, math

def vector_subtract(v, w):
    """subtracts corresponding elements """
    assert len(v) == len(w)
    return [v_i - w_i
            for v_i, w_i in zip(v, w)]

def dot (v, w):
    """v_1 * w_1 + ... + v_n * w_n"""
    return sum(v_i * w_i
                for v_i, w_i in zip(v, w))

def sum_of_squares(v):
    """ v_1 **2 + ... + v_n **2"""
    return dot(v, v)

def magnitude(v):
    return math.sqrt(sum_of_squares(v))

def squared_distance(v, w):
    """(v_i - w_1) ** 2 + ... (v_n - w_n) ** 2 """
    return sum_of_squares(vector_subtract(v, w))

def distance(v, w):
    return magnitude(vector_subtract(v, w))

def raw_majority_vote(labels):
    votes = Counter(labels)
    winner, _ = votes.most_common(1)[0]
    return winner

def majority_vote(labels):
    """ assumes that labels are ordered from nearest to farthest"""
    vote_counts = Counter(labels)
    winner, winner_count = vote_counts.most_common(1)[0]
    num_winners = len([count
                        for count in vote_counts.values()
                        if count == winner_count])
    if num_winners == 1:
        return winner
    else:
        return majority_vote(labels[:-1])

def knn_classify(k, labeled_points, new_point):
    """each labeled point should be a pair (point, label)"""

    #order the labeled points from nearest to farthest
    temp_fn =lambda point: distance(point[0], new_point)
    by_distance = sorted(labeled_points, key=temp_fn)
    # find the labels for the k clostest
    k_nearest_labels = [label for _, label in by_distance[:k]]

    #and let them vote
    return majority_vote(k_nearest_labels)

cities = [(-86.75,33.5666666666667,'Python'),
            (-88.25,30.6833333333333,'Python'),
            (-112.016666666667,33.4333333333333,'Java'),
            (-110.933333333333,32.1166666666667,'Java'),
            (-92.2333333333333,34.7333333333333,'R'),
            (-121.95,37.7,'R'),
            (-118.15,33.8166666666667,'Python'),
            (-118.233333333333,34.05,'Java'),
            (-122.316666666667,37.8166666666667,'R'),
            (-117.6,34.05,'Python'),
            (-116.533333333333,33.8166666666667,'Python'),
            (-121.5,38.5166666666667,'R'),
            (-117.166666666667,32.7333333333333,'R'),
            (-122.383333333333,37.6166666666667,'R'),
            (-121.933333333333,37.3666666666667,'R'),
            (-122.016666666667,36.9833333333333,'Python'),
            (-104.716666666667,38.8166666666667,'Python'),
            (-104.866666666667,39.75,'Python'),
            (-72.65,41.7333333333333,'R'),
            (-75.6,39.6666666666667,'Python'),
            (-77.0333333333333,38.85,'Python'),
            (-80.2666666666667,25.8,'Java'),
            (-81.3833333333333,28.55,'Java'),
            (-82.5333333333333,27.9666666666667,'Java'),
            (-84.4333333333333,33.65,'Python'),
            (-116.216666666667,43.5666666666667,'Python'),
            (-87.75,41.7833333333333,'Java'),
            (-86.2833333333333,39.7333333333333,'Java'),
            (-93.65,41.5333333333333,'Java'),
            (-97.4166666666667,37.65,'Java'),
            (-85.7333333333333,38.1833333333333,'Python'),
            (-90.25,29.9833333333333,'Java'),
            (-70.3166666666667,43.65,'R'),
            (-76.6666666666667,39.1833333333333,'R'),
            (-71.0333333333333,42.3666666666667,'R'),
            (-72.5333333333333,42.2,'R'),
            (-83.0166666666667,42.4166666666667,'Python'),
            (-84.6,42.7833333333333,'Python'),
            (-93.2166666666667,44.8833333333333,'Python'),
            (-90.0833333333333,32.3166666666667,'Java'),
            (-94.5833333333333,39.1166666666667,'Java'),
            (-90.3833333333333,38.75,'Python'),
            (-108.533333333333,45.8,'Python'),
            (-95.9,41.3,'Python'),
            (-115.166666666667,36.0833333333333,'Java'),
            (-71.4333333333333,42.9333333333333,'R'),
            (-74.1666666666667,40.7,'R'),
            (-106.616666666667,35.05,'Python'),
            (-78.7333333333333,42.9333333333333,'R'),
            (-73.9666666666667,40.7833333333333,'R'),
            (-80.9333333333333,35.2166666666667,'Python'),
            (-78.7833333333333,35.8666666666667,'Python'),
            (-100.75,46.7666666666667,'Java'),
            (-84.5166666666667,39.15,'Java'),(-81.85,41.4,'Java'),
            (-82.8833333333333,40,'Java'),(-97.6,35.4,'Python'),
            (-122.666666666667,45.5333333333333,'Python'),
            (-75.25,39.8833333333333,'Python'),
            (-80.2166666666667,40.5,'Python'),
            (-71.4333333333333,41.7333333333333,'R'),
            (-81.1166666666667,33.95,'R'),
            (-96.7333333333333,43.5666666666667,'Python'),
            (-90,35.05,'R'),
            (-86.6833333333333,36.1166666666667,'R'),
            (-97.7,30.3,'Python'),(-96.85,32.85,'Java'),
            (-95.35,29.9666666666667,'Java'),
            (-98.4666666666667,29.5333333333333,'Java'),
            (-111.966666666667,40.7666666666667,'Python'),
            (-73.15,44.4666666666667,'R'),
            (-77.3333333333333,37.5,'Python'),
            (-122.3,47.5333333333333,'Python'),
            (-89.3333333333333,43.1333333333333,'R'),
            (-104.816666666667,41.15,'Java')]

new_city_list = list()
for city in cities:
    x, y, lang = city
    new_city_list.append(([x, y], lang))
cities = new_city_list

segments = []
points = []

lat_long_regex = r"<point lat=\"(.*)\" lng=\"(.*)\""

with open("states.txt", "r") as f:
    lines = [line for line in f]

for line in lines:
    if line.startswith("</state>"):
        for p1, p2 in zip(points, points[1:]):
            segments.append((p1, p2))
        points = []
    s = re.search(lat_long_regex, line)
    if s:
        lat, lon = s.groups()
        points.append((float(lon), float(lat)))

def plot_state_borders(color='0'):
    for (lon1, lat1), (lon2, lat2) in segments:
        plt.plot([lon1, lon2], [lat1, lat2], color=color)



def plot_cities():
    #key is language, value is pair (longitude, latitude)
    plots = {"Java": ([], []), "Python" : ([], []), "R": ([], []) }

    #we want each language to have a different marker and color
    markers = {"Java": "o", "Python":"s", "R":"^"}
    colors = {"Java": "r", "Python":"b", "R": "g"}

    for longi, lati, language in cities:
        plots[language][0].append(longi)
        plots[language][1].append(lati)

    for language, (x, y) in plots.items():
        plt.scatter(x, y, c=colors[language], marker=markers[language],
                    label=language, zorder=10)

    plot_state_borders()

    plt.legend(loc=0)
    plt.axis([-130, -60, 20, 55])

    plt.title("Favorite Programming Languages")
    plt.show()

#plot_cities()

def testin_knn_cities():
    for k in range(1, 33, 2):
        num_correct = 0

        for city in cities:
            location, actual_language = city
            other_cities = [other_city
                            for other_city in cities
                            if other_city != city]
            #print(city, other_cities)
            predicted_language = knn_classify(k, other_cities, city)
            if predicted_language == actual_language:
                num_correct += 1

        print(k, "neighbor[s]:", num_correct, "correct out of", len(cities))

def decision_map_generate(k):
    plots = {"Java": ([], []), "Python" : ([], []), "R": ([], []) }

    #k = 1 #or 3, 5, 7,...

    for longi in range(-130, -60, 2):
        for lati in range(20, 55, 2):
            predicted_lang = knn_classify(k, cities, [longi, lati])
            plots[predicted_lang][0].append(longi)
            plots[predicted_lang][1].append(lati)

    return plots

def plot_decision_plot_subs():
    markers = {"Java": "o", "Python":"s", "R":"^"}
    colors = {"Java": "r", "Python":"b", "R": "g"}

    fig = plt.figure()

    plt.title("Decision Map with differing K \n using K-Nearest Neighbors")

    ax0 = fig.add_subplot(221)
    plt.title("K = 1")
    plot0 = decision_map_generate(1)
    ax1 = fig.add_subplot(222)
    plt.title("K = 3")
    plot1 = decision_map_generate(3)
    ax2 = fig.add_subplot(223)
    plt.title("K = 5")
    plot2 = decision_map_generate(5)
    ax3 = fig.add_subplot(224)
    plt.title("K = 10")
    plot3 = decision_map_generate(10)


    for language, (x, y) in plot0.items():
        ax0.scatter(x, y, c=colors[language], marker=markers[language],
                        label=language, zorder=10)
    for (lon1, lat1), (lon2, lat2) in segments:
        ax0.plot([lon1, lon2], [lat1, lat2], color="0")

    for language, (x, y) in plot1.items():
        ax1.scatter(x, y, c=colors[language], marker=markers[language],
                        label=language, zorder=10)
    for (lon1, lat1), (lon2, lat2) in segments:
        ax1.plot([lon1, lon2], [lat1, lat2], color="0")

    for language, (x, y) in plot2.items():
        ax2.scatter(x, y, c=colors[language], marker=markers[language],
                        label=language, zorder=10)
    for (lon1, lat1), (lon2, lat2) in segments:
        ax2.plot([lon1, lon2], [lat1, lat2], color="0")

    for language, (x, y) in plot3.items():
        ax3.scatter(x, y, c=colors[language], marker=markers[language],
                        label=language, zorder=10)
    for (lon1, lat1), (lon2, lat2) in segments:
        ax3.plot([lon1, lon2], [lat1, lat2], color="0")

    plt.legend(loc=0)
    ax0.axis([-130, -60, 20, 55])
    ax1.axis([-130, -60, 20, 55])
    ax2.axis([-130, -60, 20, 55])
    ax3.axis([-130, -60, 20, 55])
    plt.show()

def refactored_plot_decision_plot_subs():
    markers = {"Java": "o", "Python":"s", "R":"^"}
    colors = {"Java": "r", "Python":"b", "R": "g"}

    fig = plt.figure()

    plt.title("Decision Map with differing K using K-Nearest Neighbors", fontsize=15)

    #k = [1, 3, 5, 7, 9, 11]  #the list of k-closest neighbors to iterate through
    #section = [231, 232, 233, 234, 235, 236] # the subplot dimensions for each k

    k = [1, 3, 5, 7,]  #the list of k-closest neighbors to iterate through
    section = [221, 222, 223, 224] # the subplot dimensions for each k
    axes = list()

    for digit, k_i in zip(section, k):
        ax = fig.add_subplot(digit)
        axes.append(ax)
        plt.title(f"K = {k_i}")

    #axes = [fig.add_subplot(231), fig.add_subplot(232), fig.add_subplot(233),
    #        fig.add_subplot(234), fig.add_subplot(235), fig.add_subplot(236),]

    for ax, k_i in zip(axes, k):
        plot = decision_map_generate(k_i)
        for language, (x, y) in plot.items():
            ax.scatter(x, y, c=colors[language], marker=markers[language],
                            label=language, zorder=10)
        for (lon1, lat1), (lon2, lat2) in segments:
            ax.plot([lon1, lon2], [lat1, lat2], color="0")
        #ax.axis([-130, -60, 20, 55])

    plt.show()

refactored_plot_decision_plot_subs()
