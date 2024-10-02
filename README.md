# web-agent-collection-offline-dataset

Originally from [clippy](https://github.com/grahamannett/clippy)

This is the refactored version of the original web annotation tool and clippy integration

![wac-start](docs/assets/wac-lab-start.jpeg)

# Example of Manual Trajectory Collection:

https://github.com/grahamannett/clippy/assets/7343667/5c904fb5-1fd8-43fa-9085-63e08271a993

Video is from prior repo, need to update this video such that it is using restyled app.

# To use

# Plugins

The way you integrate datasets/agents is now via a plugin system. An example can be seen in `src/wac_lab/plugins/clippy.py` that uses a websocket to communicate with the clippy agent.

# Example Dataset

The full dataset will be available on huggingface, to use a small example until then use the following [tasks-examples.zip](https://github.com/user-attachments/files/16169267/tasks-examples.zip)

Example usage:

```bash
# assuming you are in the wac-agent-collection-offline-dataset directory
wget https://github.com/user-attachments/files/16169267/tasks-examples.zip && unzip tasks-examples.zip
mkdir -p example-data && mv tasks-examples example-data/tasks

DATA_DIR=$PWD/example-data pdm run app
```

# layout

- `src/wac_lab`
  - web app
- `src/wacommon`
  - common code for the web app, plugins and offline dataset collection
- `src/wac_plugins`
  - plugins for the web app



# dev setup

to dev setup, use pdm/uv.  There is probably a better folder layout structure as I want to have the plugins separate from the main app. Use `pip install -e src/wac_lab_app` to allow the app to be importable from either `wac_lab` or `wac_lab_app`

