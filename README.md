# flex-map

## エレベーターピッチ
現状、Google mapが提供しているルート検索は、バス・電車、車・タクシー、徒歩のみとなっている。

しかしながら、近年電動キックボードのレンタルサービスや、自転車、車のシェアリングサービスが台頭し、移動手段の多様化が進んでいる。

そのため、今後のルート検索アプリケーションには、これらの多様性に対するスケーラビリティが求められている。

我々はこの課題を解決するために、複雑化する選択肢に柔軟に対応できるプラットフォームを作成する。

## 最初にすること
- `git clone ~`
- ルートディレクトリで`docker-compose build`を実行してイメージを作成する。

## 毎回すること
- ルートディレクトリで`docker-compose up` (バックグランドで実行する場合は '-d'を付ける。)を実行してコンテナを起動する。
  - app
    - manage.pyが実行され、Djangoサーバーが立ち上がる。
    - コンテナが起動しているOSのIPアドレス:8000でサービスにアクセスできる。
    【例】
      ```
      localhost:8000/
      ```

### googleMapsAPI叩くと
- リクエスト
```
https://maps.googleapis.com/maps/api/directions/json?origin=東京駅&destination=つくばセンター&mode=DRIVING&key=APIKEY
```

- return 
```
{
  geocoded_waypoints: [
    routes: [
      {
        legs: [
          {
            distance: {
              text: "62.4km"
              value 62.4
            },
            duration: {
              text: "1 hour 4 mins"
              value 3834
            },
            end_address,
            end_location: {
              lat,
              lng
            },
            start_address,
            start_location: {
              lat,
              lng
            },
            steps: [
              {
                {
                  どこからどこまで行って，どの方向に曲がって，何分かかるかみたいな情報が入子になっている
                }
              },
              {
                  どこからどこまで行って，どの方向に曲がって，何分かかるかみたいな情報が入子になっている
              }
            ]
          }
        ]
      }
    ]
  ]
}
```
