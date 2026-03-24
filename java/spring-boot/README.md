# Spring Boot Basics

## Spring App Layers
- Presentation: camada que lida com reqs externas (\`@RestController\`)
- Service: camada que lida com regras de negocio (\`@Service\`)
- Persistence: camada que lida com os dados (\`@Repository\`)

## Dependency Injection
- Desacoplamento
- Spring gerencia dependencias
- Classes recebem dependencias de "fora"
- Codificacao baseada em contratos (\`interfaces\`)

### BEANS
- Classes concretas que implementam interfaces (\`@Component`\)
- Em caso de +1 implementacao, usa-se \`@Qualifier("str")\` ou \`@Primary\` para definir a prioridade

## Basic Annotations

- @SpringBootApplication = aliase para:
    - \`@Configuration\`;
    - \`@ComponentScan\`;
    - \`@EnableAutoConfiguration\`

- @Configuration: classe para configuracao de BEANS
- @ComponentScan: define o ponto inicial de onde os BEANS serao buscados
- @EnableAutoConfiguration: configura automaticamente a aplicacao com base nas dependencias

## Environment Variables
- server.port:8181 = SERVER_PORT=8181
- mvn: SERVER_PORT=8282 ./mvnw spring-boot:run (export SERVER_PORT=8282)
- @ConfigurationProperties(prefix = "str"): prefix no application.properties