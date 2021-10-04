# Metrics

Service collects metrics from devices and shows some charts

## Vuln 1

As we can see, access token for metric generates using known fields.

```java
public static String calculateToken(InnerMetric innerMetric) {
        String stringToHash = innerMetric.getDevice() + innerMetric.getType() +
                innerMetric.getValue() + innerMetric.getInfo();
        MessageDigest md;
        try {
            md = MessageDigest.getInstance("MD5");
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException();
        }
        md.update(stringToHash.getBytes());
        byte[] digest = md.digest();
        return DatatypeConverter.printHexBinary(digest).toUpperCase();
    }
```

So it is easy to get all metrics and their known fields. All metrics can be accessed via `GET /metrics` request. 

[sploit](../../sploits/metrics/src/main/java/HttpClientExploiter.java)

## Vuln 2

Finding metric by token uses LIKE function. 
```java
public List<InnerMetric> get(String token) {
        try (Session session = openHibernateSession()) {
            CriteriaBuilder builder = session.getCriteriaBuilder();
            CriteriaQuery<InnerMetric> query = builder.createQuery(InnerMetric.class);
            Root<InnerMetric> root = query.from(InnerMetric.class);
            query = query.where(builder.like(root.get("token"), token + "%"));
            query = query.select(root);

            return session.createQuery(query).list();
        }
    }
```
So we can just bruteforce letters from `A` to `F` and digits to get all possible metrics. Sploit is above.

