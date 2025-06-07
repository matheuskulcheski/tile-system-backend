import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { getProjects } from '@/services/projects';
import { getClients } from '@/services/clients';
import { Calendar, Users, Briefcase, Clock, AlertTriangle, CheckCircle } from 'lucide-react';
import { getCurrentUser } from '@/services/auth';

const Dashboard = () => {
  const [projects, setProjects] = useState([]);
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalProjects: 0,
    inProgressProjects: 0,
    completedProjects: 0,
    estimateProjects: 0,
    totalClients: 0,
  });
  const user = getCurrentUser();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const projectsData = await getProjects();
        const clientsData = await getClients();
        
        setProjects(projectsData.projects);
        setClients(clientsData.clients);
        
        // Calcular estatísticas
        const totalProjects = projectsData.projects.length;
        const inProgressProjects = projectsData.projects.filter(p => p.status === 'in_progress').length;
        const completedProjects = projectsData.projects.filter(p => p.status === 'completed').length;
        const estimateProjects = projectsData.projects.filter(p => p.status === 'estimate').length;
        const totalClients = clientsData.clients.length;
        
        setStats({
          totalProjects,
          inProgressProjects,
          completedProjects,
          estimateProjects,
          totalClients,
        });
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Filtrar projetos em andamento para exibição rápida
  const inProgressProjects = projects.filter(project => project.status === 'in_progress');
  
  // Filtrar projetos que precisam de orçamento
  const estimateProjects = projects.filter(project => project.status === 'estimate');

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <div>
          <p className="text-gray-600">Bem-vindo, {user?.name}</p>
        </div>
      </div>

      {/* Cards de estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total de Projetos</CardTitle>
            <Briefcase className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalProjects}</div>
            <p className="text-xs text-muted-foreground">
              {stats.inProgressProjects} em andamento
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Projetos Concluídos</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.completedProjects}</div>
            <p className="text-xs text-muted-foreground">
              {((stats.completedProjects / stats.totalProjects) * 100).toFixed(0)}% do total
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Orçamentos Pendentes</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.estimateProjects}</div>
            <p className="text-xs text-muted-foreground">
              Aguardando aprovação
            </p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total de Clientes</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalClients}</div>
            <p className="text-xs text-muted-foreground">
              Base de clientes ativos
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Projetos em andamento */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle className="text-xl">Projetos em Andamento</CardTitle>
            <CardDescription>Projetos que estão atualmente em execução</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {loading ? (
              <p>Carregando...</p>
            ) : inProgressProjects.length > 0 ? (
              inProgressProjects.slice(0, 5).map((project) => (
                <div key={project.id} className="flex justify-between items-center border-b pb-2">
                  <div>
                    <h3 className="font-medium">{project.title}</h3>
                    <p className="text-sm text-gray-500">
                      {project.installation_city}, {project.installation_state}
                    </p>
                  </div>
                  <Link to={`/projects/${project.id}`}>
                    <Button variant="outline" size="sm">Ver Detalhes</Button>
                  </Link>
                </div>
              ))
            ) : (
              <p className="text-gray-500">Nenhum projeto em andamento no momento.</p>
            )}
          </CardContent>
          <CardFooter>
            <Link to="/projects" className="w-full">
              <Button variant="outline" className="w-full">Ver Todos os Projetos</Button>
            </Link>
          </CardFooter>
        </Card>

        {/* Orçamentos pendentes */}
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle className="text-xl">Orçamentos Pendentes</CardTitle>
            <CardDescription>Orçamentos que aguardam aprovação</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {loading ? (
              <p>Carregando...</p>
            ) : estimateProjects.length > 0 ? (
              estimateProjects.slice(0, 5).map((project) => (
                <div key={project.id} className="flex justify-between items-center border-b pb-2">
                  <div>
                    <h3 className="font-medium">{project.title}</h3>
                    <p className="text-sm text-gray-500">
                      Valor: ${parseFloat(project.estimated_total).toFixed(2)}
                    </p>
                  </div>
                  <Link to={`/projects/${project.id}`}>
                    <Button variant="outline" size="sm">Ver Detalhes</Button>
                  </Link>
                </div>
              ))
            ) : (
              <p className="text-gray-500">Nenhum orçamento pendente no momento.</p>
            )}
          </CardContent>
          <CardFooter>
            <Link to="/estimates" className="w-full">
              <Button variant="outline" className="w-full">Ver Todos os Orçamentos</Button>
            </Link>
          </CardFooter>
        </Card>
      </div>

      {/* Ações rápidas */}
      <Card>
        <CardHeader>
          <CardTitle className="text-xl">Ações Rápidas</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Link to="/clients/new">
              <Button variant="outline" className="w-full h-24 flex flex-col items-center justify-center">
                <Users className="h-6 w-6 mb-2" />
                <span>Novo Cliente</span>
              </Button>
            </Link>
            <Link to="/projects/new">
              <Button variant="outline" className="w-full h-24 flex flex-col items-center justify-center">
                <Briefcase className="h-6 w-6 mb-2" />
                <span>Novo Projeto</span>
              </Button>
            </Link>
            <Link to="/estimates/new">
              <Button variant="outline" className="w-full h-24 flex flex-col items-center justify-center">
                <AlertTriangle className="h-6 w-6 mb-2" />
                <span>Novo Orçamento</span>
              </Button>
            </Link>
            <Link to="/schedule">
              <Button variant="outline" className="w-full h-24 flex flex-col items-center justify-center">
                <Calendar className="h-6 w-6 mb-2" />
                <span>Agenda</span>
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;

