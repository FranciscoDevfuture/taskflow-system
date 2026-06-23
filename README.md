# 🚀 TaskFlow System

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

> Uma API RESTful para gerenciamento ágil de tarefas, desenvolvida com Flask e boas práticas de Engenharia de Software.

## 📋 Sobre o Projeto

O **TaskFlow System** é uma API de gerenciamento de tarefas que permite autenticação de usuários, CRUD completo de tarefas, filtros por status e prioridade, além de contar com testes automatizados e integração contínua. Foi desenvolvido como parte do curso de Engenharia de Software na Unifecaf.

### 🎯 Principais Funcionalidades

- ✅ **Autenticação segura**: Login e logout com sessão Flask
- ✅ **CRUD completo de tarefas**: Criar, listar, atualizar e deletar tarefas
- ✅ **Filtros avançados**: Por status (`a_fazer`, `em_progresso`, `concluido`) e prioridade (`baixa`, `media`, `alta`, `critica`)
- ✅ **Validações robustas**: Campos obrigatórios, transições de status válidas e regras de negócio
- ✅ **Testes automatizados**: 85 testes com Pytest
- ✅ **CI/CD**: Pipeline automatizado com GitHub Actions

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|------------|
| **Python 3.14** | Linguagem de programação |
| **Flask** | Framework web |
| **SQLite** | Banco de dados (em memória para testes) |
| **Pytest** | Testes automatizados |
| **GitHub Actions** | Integração contínua |
| **Postman** | Testes manuais da API |

## 📁 Estrutura do Projeto
