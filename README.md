# Example Project

This example project is developed to monitor the music activity in channels.

## Requirements
- Docker
- docker-compose
- Make

## Build
```
make build
make up
```

## Test
After build is finished, you can test the app with the following command
```
make test
```

## Questions
### Design Choices
- This project uses `flask` library for rest api since it is a lightweight library and gives developer enough freedom for customization.

- As DB, `postgresql` is used. It is a production ready, and highly used database among folk. Because of these, this db is used.

- Four different tables are used: `Channel`, `Performer`, `Song` and `Play`. 
    - `Song` is in relation with `Performer`
    - `Play` is in relation with both `Song` and `Channel`.

- This table strucure reflects natural relationship between these entities. This natural structure enpowers developer to further extend their query easily if needed. 
