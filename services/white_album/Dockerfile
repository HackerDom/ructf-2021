FROM mcr.microsoft.com/dotnet/sdk:5.0 AS builder
LABEL stage=builder

COPY ./src /app

WORKDIR /app

RUN dotnet restore && dotnet publish -c Release -o publish

FROM mcr.microsoft.com/dotnet/aspnet:5.0

WORKDIR /app

COPY --from=0 /app ./

RUN adduser --system --home /app --shell /usr/sbin/nologin --no-create-home --disabled-password deployer

CMD ["dotnet", "publish/WhiteAlbum.dll"]