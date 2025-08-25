# Let Him Cook 🍳

A fun cooking simulation game where you manage a kitchen, prepare ingredients, and serve customers! Take on the role of a chef and see how many orders you can complete.

## 🎮 Game Overview

"Let Him Cook" is a pixel-art cooking game where players manage a kitchen workspace, interact with various cooking stations, and prepare delicious meals for customers. The game features a day/night cycle with cooking waves and break periods.

## 🚀 Features

- **Kitchen Management**: Build and place various cooking stations
- **Ingredient System**: Collect, combine, and process ingredients
- **Recipe Crafting**: Create complex dishes by combining ingredients
- **Building System**: Purchase and place new kitchen equipment
- **Day/Night Cycle**: Manage your kitchen during cooking and break waves
- **Customer Service**: Sell completed dishes for profit
- **Inventory Management**: Limited inventory space adds strategic depth

## 🎯 How to Play

### Controls
- **WASD** or **Arrow Keys**: Move your character
- **E**: Interact with buildings (place items, open menus)
- **Q** or **Right Ctrl**: Pick up items from buildings
- **Space**: Add random ingredients to inventory (debug feature)
- **Escape**: Pause game or return to previous menu

### Gameplay Loop
1. **Break Wave**: Purchase new buildings and ingredients
2. **Cooking Wave**: Serve customers and complete orders
3. **Manage Resources**: Balance money, inventory space, and customer demands


## 🎥 Video Demonstration

**Watch the full gameplay demonstration:**

### Option 1: Download and View
[📥 Download Let_Him_Cook.mp4](readmePics/video/Let_Him_Cook.mp4)

### Option 2: GitHub Video Upload
To make the video play directly in GitHub, you need to:

1. **Upload your MP4 file** to GitHub Issues or Discussions
2. **Copy the generated URL** from the uploaded video
3. **Replace the link below** with your actual GitHub video URL

**Current video file:** `readmePics/video/Let_Him_Cook.mp4`

*Note: For the video to auto-play in GitHub, it needs to be uploaded through GitHub's interface, not just stored in your repository.*

---

**Video Features Showcased:**
- 🍳 Real-time cooking mechanics
- 🏗️ Kitchen building system
- 🛒 Shop and decoration features
- 📦 Inventory management
- 👥 Multiplayer gameplay

## 🎯 Core Gameplay Features

### **Project Overview:**
"Let Him Cook" is an innovative multiplayer cooking simulation game that combines strategic kitchen management with real-time culinary challenges. Players work together (or compete) to build, manage, and optimize their kitchen operations while serving customers under time pressure.

#### 1. **Stack Food & Create Dishes Using Built-in Recipes Within Cooking Time**

![Core Cooking Mechanics](readmePics/cooking-mechanics.png)

- **Real-time Cooking System**: Players must efficiently stack ingredients and create dishes using built-in recipes while racing against the clock
- **Recipe Management**: Comprehensive recipe system with ingredients like meat, tomato, lettuce, cheese, and more
- **Time Pressure**: "COOKIN TIME" countdown creates intense, engaging gameplay where every second counts
- **Ingredient Combination**: Strategic stacking of ingredients at various cooking stations to maximize efficiency

#### 2. **Customizable Kitchen Building System**

![Kitchen Building System](readmePics/kitchen-building.png)

- **Freedom of Design**: Players can build their kitchen exactly how they want with complete freedom of placement
- **Modular Construction**: Various building types including counters, processors, storage units, and decorative elements
- **Strategic Layout**: Optimize kitchen flow for maximum efficiency and customer satisfaction
- **Building Categories**: From basic counters ($10) to advanced processors ($100) and premium storage ($1000)

#### 3. **Comprehensive Shop & Decoration System**

![Shop & Decoration System](readmePics/shop-system.png)

- **Ingredient Shop**: Purchase fresh ingredients like meat, vegetables, dairy, and spices
- **Equipment Store**: Buy cooking appliances including ovens, choppers, grills, and specialized tools
- **Decoration Items**: Customize your kitchen with aesthetic elements and functional decorations
- **Progressive Unlocking**: Unlock new items and buildings as you earn money and progress

#### 4. **Advanced Inventory Management**

![Inventory Management System](readmePics/inventory-system.png)

- **Smart Storage**: Store items in organized inventory systems with capacity management
- **Multi-tier Storage**: From personal inventory (10 slots) to fridge storage (20 slots)
- **Item Organization**: Efficiently manage ingredients, prepared dishes, and cooking tools
- **Quick Access**: Streamlined interface for rapid ingredient selection and combination

#### 5. **Multiplayer Collaboration & Competition**

![Multiplayer Experience](readmePics/multiplayer.png)

- **Cooperative Play**: Work together with friends to build the ultimate kitchen
- **Competitive Mode**: Race against other players to complete orders and earn profits
- **Shared Resources**: Collaborate on kitchen expansion and recipe development
- **Social Interaction**: Build, cook, and succeed together in a shared culinary world

### 🏗️ Technical Implementation

**Game Engine**: Built with Python and Pygame for cross-platform compatibility
**Multiplayer Architecture**: Real-time synchronization for seamless cooperative gameplay
**Procedural Generation**: Dynamic recipe and challenge generation for endless replayability
**Performance Optimization**: Efficient rendering and physics for smooth multiplayer experience

### 🎮 Gameplay Mechanics

**Cooking Stations:**
- **Counters**: Basic food preparation and ingredient combination
- **Processors**: Specialized equipment for cutting, cooking, and processing
- **Storage Units**: Organized ingredient and dish storage
- **Serving Areas**: Customer interaction and order fulfillment

**Recipe System:**
- **Counter Recipes**: Burgers, salads, and basic combinations
- **Oven Recipes**: Baked goods and cooked dishes
- **Chopper Recipes**: Ingredient preparation and cutting
- **Advanced Combinations**: Multi-step recipes requiring multiple stations

**Economy & Progression:**
- **Starting Capital**: $500 to begin kitchen construction
- **Income Generation**: Sell completed dishes to customers
- **Investment Strategy**: Balance immediate needs with long-term kitchen expansion
- **Goal Achievement**: Reach daily targets and unlock new content


## 🎨 Technical Details

### Built With
- **Python 3.x**
- **Pygame**: Game engine and graphics
- **Pixel Art**: Custom sprites and animations

### Project Structure
```
Let-Him-Cook/
├── main.py              # Main game entry point
├── game.py              # Core game logic
├── player.py            # Player character and controls
├── world.py             # World generation and buildings
├── items.py             # Item and inventory system
├── userinterface.py     # UI components and menus
├── worldEditor.py       # Building placement system
├── sprites/             # Game sprites and textures
├── sounds/              # Audio files
├── fonts/               # Custom fonts
└── tests/               # Unit tests
```

## 🧪 Testing

The project includes comprehensive unit tests for core mechanics:

```bash
# Run all tests
python3 -m unittest discover -s tests -p 'test_*.py' -v

# Run specific test file
python3 -m unittest tests.test_pickup_drop -v
```

### Test Coverage
- **Pickup Mechanics**: Testing item retrieval from buildings
- **Drop Mechanics**: Testing item placement on cooking stations
- **Inventory Management**: Testing capacity limits and item handling
- **Building Interactions**: Testing various cooking station behaviors


### 🌟 Innovation & Impact

**Unique Features:**
- **Real-time Multiplayer Cooking**: First-of-its-kind collaborative kitchen management
- **Dynamic Recipe System**: Adaptive challenges based on player skill and kitchen setup
- **Strategic Building**: Deep customization system for kitchen optimization
- **Time Management**: Engaging gameplay that rewards both speed and strategy

**Educational Value:**
- **Culinary Knowledge**: Learn about ingredient combinations and cooking techniques
- **Resource Management**: Develop strategic thinking and planning skills
- **Team Collaboration**: Practice communication and coordination in multiplayer
- **Business Management**: Understand basic economics and investment strategies

### 🚀 Future Development

**Planned Features:**
- **Mobile Version**: Cross-platform mobile compatibility
- **VR Support**: Immersive virtual reality kitchen experience
- **AI Chefs**: Intelligent NPCs for single-player mode
- **Seasonal Events**: Special challenges and limited-time content
- **Community Features**: Recipe sharing and kitchen showcase system

**Technical Roadmap:**
- **Cloud Saves**: Cross-device progress synchronization
- **Modding Support**: Community-created content and recipes
- **Analytics Dashboard**: Player performance and kitchen optimization insights
- **API Integration**: Connect with real-world recipe databases

---

**"Let Him Cook" represents the future of collaborative gaming, combining the creativity of building games with the excitement of real-time challenges and the social aspects of multiplayer cooperation. It's not just a game—it's a culinary adventure that brings people together to create, compete, and cook!** 🍳✨

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Pygame library

### Installation
1. Clone the repository:
   ```bash
   git clone [your-repo-url]
   cd Let-Him-Cook
   ```

2. Install dependencies:
   ```bash
   pip install pygame
   ```

3. Run the game:
   ```bash
   python3 main.py
   ```

## 🎯 Game Objectives

- **Short Term**: Complete customer orders efficiently
- **Medium Term**: Expand kitchen with new equipment
- **Long Term**: Master all recipes and maximize profits

**Let Him Cook** - Where culinary creativity meets strategic gameplay! 🍽️
