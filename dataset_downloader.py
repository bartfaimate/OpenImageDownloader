#! /usr/bin/python3

import requests
import json
import argparse
import time
import os
import sys

CLASSES = [
    "Accordion", "Adhesive tape", "Aircraft", "Airplane", "Alarm clock", "Alpaca", "Ambulance", "Animal", "Ant", "Antelope", "Apple", "Armadillo", "Artichoke", "Auto part", "Axe", "Backpack", "Bagel", "Baked goods", "Balance beam", "Ball", "Balloon", "Banana", "Band-aid", "Banjo", "Barge", "Barrel", "Baseball bat", "Baseball glove", "Bat (Animal)", "Bathroom accessory", "Bathroom cabinet", "Bathtub", "Beaker", "Bear", "Bed", "Bee", "Beehive", "Beer", "Beetle", "Bell pepper", "Belt", "Bench", "Bicycle", "Bicycle helmet", "Bicycle wheel", "Bidet", "Billboard", "Billiard table", "Binoculars", "Bird", "Blender", "Blue jay", "Boat", "Bomb", "Book", "Bookcase", "Boot", "Bottle", "Bottle opener", "Bow and arrow", "Bowl", "Bowling equipment", "Box", "Boy", "Brassiere", "Bread", "Briefcase", "Broccoli", "Bronze sculpture", "Brown bear", "Building", "Bull", "Burrito", "Bus", "Bust", "Butterfly", "Cabbage", "Cabinetry", "Cake", "Cake stand", "Calculator", "Camel", "Camera", "Can opener", "Canary", "Candle", "Candy", "Cannon", "Canoe", "Cantaloupe", "Car", "Carnivore", "Carrot", "Cart", "Cassette deck", "Castle", "Cat", "Cat furniture", "Caterpillar", "Cattle", "Ceiling fan", "Cello", "Centipede", "Chainsaw", "Chair", "Cheese", "Cheetah", "Chest of drawers", "Chicken", "Chime", "Chisel", "Chopsticks", "Christmas tree", "Clock", "Closet", "Clothing", "Coat", "Cocktail", "Cocktail shaker", "Coconut", "Coffee", "Coffee cup", "Coffee table", "Coffeemaker", "Coin", "Common fig", "Common sunflower", "Computer keyboard", "Computer monitor", "Computer mouse", "Container", "Convenience store", "Cookie", "Cooking spray", "Corded phone", "Cosmetics", "Couch", "Countertop", "Cowboy hat", "Crab", "Cream", "Cricket ball", "Crocodile", "Croissant", "Crown", "Crutch", "Cucumber", "Cupboard", "Curtain", "Cutting board", "Dagger", "Dairy Product", "Deer", "Desk", "Dessert", "Diaper", "Dice", "Digital clock", "Dinosaur", "Dishwasher", "Dog", "Dog bed", "Doll", "Dolphin", "Door", "Door handle", "Doughnut", "Dragonfly", "Drawer", "Dress", "Drill (Tool)", "Drink", "Drinking straw", "Drum", "Duck", "Dumbbell", "Eagle", "Earrings", "Egg (Food)", "Elephant", "Envelope", "Eraser", "Face powder", "Facial tissue holder", "Falcon", "Fashion accessory", "Fast food", "Fax", "Fedora", "Filing cabinet", "Fire hydrant", "Fireplace", "Fish", "Flag", "Flashlight", "Flower", "Flowerpot", "Flute", "Flying disc", "Food", "Food processor", "Football", "Football helmet", "Footwear", "Fork", "Fountain", "Fox", "French fries", "French horn", "Frog", "Fruit", "Frying pan", "Furniture", "Garden Asparagus", "Gas stove", "Giraffe", "Girl", "Glasses", "Glove", "Goat", "Goggles", "Goldfish", "Golf ball", "Golf cart", "Gondola", "Goose", "Grape", "Grapefruit", "Grinder", "Guacamole", "Guitar", "Hair dryer", "Hair spray", "Hamburger", "Hammer", "Hamster", "Hand dryer", "Handbag", "Handgun", "Harbor seal", "Harmonica", "Harp", "Harpsichord", "Hat", "Headphones", "Heater", "Hedgehog", "Helicopter", "Helmet", "High heels", "Hiking equipment", "Hippopotamus", "Home appliance", "Honeycomb", "Horizontal bar", "Horse", "Hot dog", "House", "Houseplant", "Human arm", "Human beard", "Human body", "Human ear", "Human eye", "Human face", "Human foot", "Human hair", "Human hand", "Human head", "Human leg", "Human mouth", "Human nose", "Humidifier", "Ice cream", "Indoor rower", "Infant bed", "Insect", "Invertebrate", "Ipod", "Isopod", "Jacket", "Jacuzzi", "Jaguar (Animal)", "Jeans", "Jellyfish", "Jet ski", "Jug", "Juice", "Kangaroo", "Kettle", "Kitchen & dining room table", "Kitchen appliance", "Kitchen knife", "Kitchen utensil", "Kitchenware", "Kite", "Knife", "Koala", "Ladder", "Ladle", "Ladybug", "Lamp", "Land vehicle", "Lantern", "Laptop", "Lavender (Plant)", "Lemon", "Leopard", "Light bulb", "Light switch", "Lighthouse", "Lily", "Limousine", "Lion", "Lipstick", "Lizard", "Lobster", "Loveseat", "Luggage and bags", "Lynx", "Magpie", "Mammal", "Man", "Mango", "Maple", "Maracas", "Marine invertebrates", "Marine mammal", "Measuring cup", "Mechanical fan", "Medical equipment", "Microphone", "Microwave oven", "Milk", "Miniskirt", "Mirror", "Missile", "Mixer", "Mixing bowl", "Mobile phone", "Monkey", "Moths and butterflies", "Motorcycle", "Mouse", "Muffin", "Mug", "Mule", "Mushroom", "Musical instrument", "Musical keyboard", "Nail (Construction)", "Necklace", "Nightstand", "Oboe", "Office building", "Office supplies", "Orange", "Organ (Musical Instrument)", "Ostrich", "Otter", "Oven", "Owl", "Oyster", "Paddle", "Palm tree", "Pancake", "Panda", "Paper cutter", "Paper towel", "Parachute", "Parking meter", "Parrot", "Pasta", "Pastry", "Peach", "Pear", "Pen", "Pencil case", "Pencil sharpener", "Penguin", "Perfume", "Person", "Personal care", "Personal flotation device", "Piano", "Picnic basket", "Picture frame", "Pig", "Pillow", "Pineapple", "Pitcher (Container)", "Pizza", "Pizza cutter", "Plant", "Plastic bag", "Plate", "Platter", "Plumbing fixture", "Polar bear", "Pomegranate", "Popcorn", "Porch", "Porcupine", "Poster", "Potato", "Power plugs and sockets", "Pressure cooker", "Pretzel", "Printer", "Pumpkin", "Punching bag", "Rabbit", "Raccoon", "Racket", "Radish", "Ratchet (Device)", "Raven", "Rays and skates", "Red panda", "Refrigerator", "Remote control", "Reptile", "Rhinoceros", "Rifle", "Ring binder", "Rocket", "Roller skates", "Rose", "Rugby ball", "Ruler", "Salad", "Salt and pepper shakers", "Sandal", "Sandwich", "Saucer", "Saxophone", "Scale", "Scarf", "Scissors", "Scoreboard", "Scorpion", "Screwdriver", "Sculpture", "Sea lion", "Sea turtle", "Seafood", "Seahorse", "Seat belt", "Segway", "Serving tray", "Sewing machine", "Shark", "Sheep", "Shelf", "Shellfish", "Shirt", "Shorts", "Shotgun", "Shower", "Shrimp", "Sink", "Skateboard", "Ski", "Skirt", "Skull", "Skunk", "Skyscraper", "Slow cooker", "Snack", "Snail", "Snake", "Snowboard", "Snowman", "Snowmobile", "Snowplow", "Soap dispenser", "Sock", "Sofa bed", "Sombrero", "Sparrow", "Spatula", "Spice rack", "Spider", "Spoon", "Sports equipment", "Sports uniform", "Squash (Plant)", "Squid", "Squirrel", "Stairs", "Stapler", "Starfish", "Stationary bicycle", "Stethoscope", "Stool", "Stop sign", "Strawberry", "Street light", "Stretcher", "Studio couch", "Submarine", "Submarine sandwich", "Suit", "Suitcase", "Sun hat", "Sunglasses", "Surfboard", "Sushi", "Swan", "Swim cap", "Swimming pool", "Swimwear", "Sword", "Syringe", "Table", "Table tennis racket", "Tablet computer", "Tableware", "Taco", "Tank", "Tap", "Tart", "Taxi", "Tea", "Teapot", "Teddy bear", "Telephone", "Television", "Tennis ball", "Tennis racket", "Tent", "Tiara", "Tick", "Tie", "Tiger", "Tin can", "Tire", "Toaster", "Toilet", "Toilet paper", "Tomato", "Tool", "Toothbrush", "Torch", "Tortoise", "Towel", "Tower", "Toy", "Traffic light", "Traffic sign", "Train", "Training bench", "Treadmill", "Tree", "Tree house", "Tripod", "Trombone", "Trousers", "Truck", "Trumpet", "Turkey", "Turtle", "Umbrella", "Unicycle", "Van", "Vase", "Vegetable", "Vehicle", "Vehicle registration plate", "Violin", "Volleyball (Ball)", "Waffle", "Waffle iron", "Wall clock", "Wardrobe", "Washing machine", "Waste container", "Watch", "Watercraft", "Watermelon", "Weapon", "Whale", "Wheel", "Wheelchair", "Whisk", "Whiteboard", "Willow", "Window", "Window blind", "Wine", "Wine glass", "Wine rack", "Winter melon", "Wok", "Woman", "Wood-burning stove", "Woodpecker", "Worm", "Wrench", "Zebra", "Zucchini",
]

def print_classes(classes):
    for i, c in enumerate(classes):
        print(f"{c:30}", end="")
        if i % 3 == 0:
            print()

def info(msg):
    """
    prints [INFO] + msg
    """
    print("[INFO] " + msg)


def main():
    """
    main function
    """
    # create argument parser
    parser = argparse.ArgumentParser(description="This is a simple dataset downloader, which app can donload images"
                                                 " from open image dataset")
    parser.add_argument("-c", "--category", help="Desired class you want to download",
                        required=False)
    parser.add_argument("-l", "--list", help="List all categories",
                        action="store_true", required=False, default=False)
    parser.add_argument("-d", "--dest", help="Destination folder", 
                        required=False, default=".")
    parser.add_argument("-n", "--maximum-number", help="Maximum number of images to download",
                         required=False, default=100, type=int)
    args = parser.parse_args()
    
    if args.list:
        # print out classes
        print_classes(CLASSES)
    elif args.category:
        # if category selected download it
        if not args.dest:
            parser.print_help()
            parser.print_usage()
            raise ValueError("Wrong argument is given")
       
        # get the categories as json
        category = args.category
        info("Starting... ")
        info(f"Downloading into {args.dest}")
        categories_query = "https://storage.googleapis.com/openimages/web/visualizer/annotations_detection_train/categ2name.json"
        response = requests.get(categories_query)
        info("Getting categories....")

        # save the json file
        classes_json = "classes.json"
        f = open(classes_json, "w")
        f.write(response.text)
        f.close()

        # open json and load into a dict
        f = open(classes_json, "r")
        content = f.read()
        classes = json.loads(content)
        f.close()

        # convert {idx: class_name} to {class_name: idx}
        new_classes = {}
        for idx in classes:
            # replace '/' with '_' because the request contains '_'
            new_classes[classes[idx]] = f"{idx.replace('/', '_')}.json"

        # create query to get the desired class
        image_query = f"https://storage.googleapis.com/openimages/web/visualizer/annotations_detection_train/{new_classes[args.category]}"
        r = requests.get(image_query)

        content = r.text
        # get the image urls and the BBoxes for the class
        image_urls = {}
        map = json.loads(content)
        for key_ in list(dict(map).keys()): 
            print(map[key_]["image"]["url_full_res"])
            bounding_boxes = []
            for obj in list(map[key_]["objects"]):
                if obj["text"] == category:
                    print(obj["bounding_box"])
                    bounding_boxes.append(obj["bounding_box"])
            image_urls[map[key_]["image"]["url_full_res"]] = bounding_boxes


        # convert 
        image_urls[list(image_urls.keys())[1]]
        original_images = list(image_urls.keys())
        num_of_images = len(original_images)

        info("Downloading images...")
        print("[", end="")

        # create directory if not exists
        if not os.path.exists(f"{args.dest}/{args.category}"):
            os.mkdir(f"{args.dest}/{args.category}")

        # download images
        # label file
        label_file = open(f"{args.dest}/{args.category}/{category}.label", "w")
        label_file.write("url,xmax,xmin,ymax,ymin,class\n")
        for i, url in enumerate(image_urls):
            if i % 15 == 0:
                # print(i)
                print("=", end="")
                sys.stdout.flush()
            if i == args.maximum_number:
                break
            
            # print(f"Getting {i}. image")
            #download the image
            r = requests.get(url)
            name = url.split("/")[-1]
            img_file = open(f"{args.dest}/{args.category}/{name}", "wb")
            img_file.write(r.content)
            img_file.close()
            
            # get the Bboxes
            for bb in image_urls[url]:
                xmax,xmin,ymax,ymin = bb["xmax"], bb["xmin"], bb["ymax"], bb["ymin"]
                label_file.write(f"{name},{xmax},{xmin},{ymax},{ymin},{args.category}\n")
        label_file.close()
        print("]")
        info("Finished downloading images")

        
            
            
if __name__ == '__main__':
   main()
    # print_classes(CLASSES)
