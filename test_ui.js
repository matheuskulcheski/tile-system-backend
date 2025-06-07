// Teste de interface do usuário para o sistema de gerenciamento de instalação de tile
// Este script simula interações do usuário com a interface

const puppeteer = require('puppeteer');

// Configurações
const BASE_URL = 'http://localhost:5173';
const TEST_EMAIL = 'owner@tilesystem.com';
const TEST_PASSWORD = 'password123';

// Cores para saída no terminal
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  underscore: '\x1b[4m',
  blink: '\x1b[5m',
  reverse: '\x1b[7m',
  hidden: '\x1b[8m',
  
  black: '\x1b[30m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
};

// Funções auxiliares
function printHeader(text) {
  console.log(`\n${colors.magenta}${colors.bright}${'='.repeat(50)}${colors.reset}`);
  console.log(`${colors.magenta}${colors.bright}${text.padStart(25 + Math.floor(text.length/2), ' ')}${colors.reset}`);
  console.log(`${colors.magenta}${colors.bright}${'='.repeat(50)}${colors.reset}\n`);
}

function printResult(success, message) {
  if (success) {
    console.log(`${colors.green}✓ ${message}${colors.reset}`);
  } else {
    console.log(`${colors.red}✗ ${message}${colors.reset}`);
  }
}

// Testes
async function runTests() {
  printHeader('Iniciando Testes de Interface');
  
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    
    // Teste de login
    await testLogin(page);
    
    // Teste de navegação no dashboard
    await testDashboard(page);
    
    // Teste de listagem de clientes
    await testClientList(page);
    
    // Teste de listagem de projetos
    await testProjectList(page);
    
    printHeader('Testes Concluídos');
    console.log(`${colors.green}${colors.bright}Todos os testes foram executados.${colors.reset}`);
    
  } catch (error) {
    console.error(`${colors.red}${colors.bright}Erro durante os testes: ${error.message}${colors.reset}`);
  } finally {
    await browser.close();
  }
}

async function testLogin(page) {
  printHeader('Teste de Login');
  
  try {
    // Navegar para a página de login
    await page.goto(`${BASE_URL}/login`);
    printResult(true, 'Navegação para página de login');
    
    // Preencher formulário de login
    await page.waitForSelector('input[type="email"]');
    await page.type('input[type="email"]', TEST_EMAIL);
    await page.type('input[type="password"]', TEST_PASSWORD);
    printResult(true, 'Preenchimento do formulário de login');
    
    // Clicar no botão de login
    await Promise.all([
      page.waitForNavigation(),
      page.click('button[type="submit"]')
    ]);
    
    // Verificar se o login foi bem-sucedido
    const currentUrl = page.url();
    if (currentUrl === `${BASE_URL}/` || currentUrl === `${BASE_URL}`) {
      printResult(true, 'Login bem-sucedido, redirecionado para o dashboard');
    } else {
      printResult(false, `Login falhou, URL atual: ${currentUrl}`);
    }
  } catch (error) {
    printResult(false, `Erro no teste de login: ${error.message}`);
    throw error; // Propagar o erro para interromper os testes
  }
}

async function testDashboard(page) {
  printHeader('Teste do Dashboard');
  
  try {
    // Verificar elementos do dashboard
    await page.waitForSelector('h1');
    const dashboardTitle = await page.$eval('h1', el => el.textContent);
    
    if (dashboardTitle.includes('Dashboard')) {
      printResult(true, 'Título do dashboard encontrado');
    } else {
      printResult(false, `Título do dashboard não encontrado. Texto atual: ${dashboardTitle}`);
    }
    
    // Verificar estatísticas
    const statsElements = await page.$$('div[class*="card"]');
    if (statsElements.length > 0) {
      printResult(true, `${statsElements.length} cards de estatísticas encontrados`);
    } else {
      printResult(false, 'Nenhum card de estatística encontrado');
    }
    
  } catch (error) {
    printResult(false, `Erro no teste do dashboard: ${error.message}`);
  }
}

async function testClientList(page) {
  printHeader('Teste de Listagem de Clientes');
  
  try {
    // Navegar para a página de clientes
    await Promise.all([
      page.waitForNavigation(),
      page.click('a[href="/clients"]')
    ]);
    
    // Verificar se estamos na página de clientes
    const currentUrl = page.url();
    if (currentUrl === `${BASE_URL}/clients`) {
      printResult(true, 'Navegação para página de clientes');
    } else {
      printResult(false, `Navegação para página de clientes falhou, URL atual: ${currentUrl}`);
      return;
    }
    
    // Verificar se a tabela de clientes existe
    await page.waitForSelector('table');
    const tableExists = await page.$('table') !== null;
    printResult(tableExists, 'Tabela de clientes encontrada');
    
    // Verificar se há clientes listados
    const rows = await page.$$('table tbody tr');
    if (rows.length > 0) {
      printResult(true, `${rows.length} clientes encontrados na tabela`);
    } else {
      printResult(false, 'Nenhum cliente encontrado na tabela');
    }
    
  } catch (error) {
    printResult(false, `Erro no teste de listagem de clientes: ${error.message}`);
  }
}

async function testProjectList(page) {
  printHeader('Teste de Listagem de Projetos');
  
  try {
    // Navegar para a página de projetos
    await Promise.all([
      page.waitForNavigation(),
      page.click('a[href="/projects"]')
    ]);
    
    // Verificar se estamos na página de projetos
    const currentUrl = page.url();
    if (currentUrl === `${BASE_URL}/projects`) {
      printResult(true, 'Navegação para página de projetos');
    } else {
      printResult(false, `Navegação para página de projetos falhou, URL atual: ${currentUrl}`);
      return;
    }
    
    // Verificar se a tabela de projetos existe
    await page.waitForSelector('table');
    const tableExists = await page.$('table') !== null;
    printResult(tableExists, 'Tabela de projetos encontrada');
    
    // Verificar se há projetos listados
    const rows = await page.$$('table tbody tr');
    if (rows.length > 0) {
      printResult(true, `${rows.length} projetos encontrados na tabela`);
    } else {
      printResult(false, 'Nenhum projeto encontrado na tabela');
    }
    
  } catch (error) {
    printResult(false, `Erro no teste de listagem de projetos: ${error.message}`);
  }
}

// Executar os testes
runTests().catch(console.error);

