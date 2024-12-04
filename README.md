
# CargoBeacon

**CargoBeacon** is a Python script that collects telemetry data from Euro Truck Simulator 2 and creates a Discord Rich Presence showing the player's location and the cargo they are hauling. This project is based on the ideas from the repository [ets2-ats-custom-discord-rich-presence](https://github.com/Shetty073/ets2-ats-custom-discord-rich-presence) and uses the [ets2-telemetry-server](https://github.com/Funbit/ets2-telemetry-server) as a dependency.

## Description

With **CargoBeacon**, you can:

- Get your location data in Euro Truck Simulator 2.
- View the cargo you are transporting.
- Display this data as a Discord Rich Presence for others to see.

## Installation

### 1. Install Dependencies

To use **CargoBeacon**, you need to install the [ets2-telemetry-server](https://github.com/Funbit/ets2-telemetry-server) which collects the necessary telemetry data from Euro Truck Simulator 2.

1. Go to the [ets2-telemetry-server](https://github.com/Funbit/ets2-telemetry-server) repository.
2. Follow the instructions for setting up and running the **ets2-telemetry-server**.

### 2. Clone the Repository

After setting up the telemetry server, clone the **CargoBeacon** repository:

```bash
git clone https://github.com/your-repository/CargoBeacon.git
cd CargoBeacon
```

### 3. Install Python Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Configuration

- Ensure the **ets2-telemetry-server** is running and transmitting data to the port specified in the **CargoBeacon** configuration file.
- Check the **config.json** file for setting the correct port and other parameters as needed.

## Usage

To start the script, run:

```bash
python main.py
```

This will begin collecting telemetry data and displaying it as Discord Rich Presence.

## How It Works

- **CargoBeacon** connects to the **ets2-telemetry-server** to retrieve player location, cargo, and other parameters.
- The gathered data is then used to update the Discord Rich Presence, showing information about your progress in the game.

## License

It will be added in the near future
