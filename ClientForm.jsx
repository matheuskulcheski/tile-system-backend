import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getClient, createClient, updateClient } from '@/services/clients';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/components/ui/use-toast';
import { ArrowLeft, Save } from 'lucide-react';

const ClientForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();
  const isEditing = !!id;

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    referral_source: '',
    notes: '',
  });

  const [loading, setLoading] = useState(false);
  const [fetchingClient, setFetchingClient] = useState(isEditing);

  useEffect(() => {
    if (isEditing) {
      fetchClient();
    }
  }, [id]);

  const fetchClient = async () => {
    try {
      setFetchingClient(true);
      const response = await getClient(id);
      setFormData(response.client);
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Erro',
        description: 'Não foi possível carregar os dados do cliente.',
      });
      navigate('/clients');
    } finally {
      setFetchingClient(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isEditing) {
        await updateClient(id, formData);
        toast({
          title: 'Cliente atualizado',
          description: 'Os dados do cliente foram atualizados com sucesso.',
        });
      } else {
        await createClient(formData);
        toast({
          title: 'Cliente criado',
          description: 'O cliente foi criado com sucesso.',
        });
      }
      navigate('/clients');
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Erro',
        description: error.message || 'Ocorreu um erro ao salvar os dados do cliente.',
      });
    } finally {
      setLoading(false);
    }
  };

  if (fetchingClient) {
    return (
      <div className="flex justify-center items-center h-64">
        <p>Carregando dados do cliente...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center">
        <Button variant="ghost" onClick={() => navigate('/clients')} className="mr-4">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Voltar
        </Button>
        <h1 className="text-2xl font-bold">{isEditing ? 'Editar Cliente' : 'Novo Cliente'}</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>{isEditing ? 'Editar informações do cliente' : 'Adicionar novo cliente'}</CardTitle>
          <CardDescription>
            Preencha os dados do cliente nos campos abaixo.
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="name">Nome completo *</Label>
                <Input
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone">Telefone *</Label>
                <Input
                  id="phone"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email || ''}
                  onChange={handleChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="referral_source">Fonte de Indicação</Label>
                <Input
                  id="referral_source"
                  name="referral_source"
                  value={formData.referral_source || ''}
                  onChange={handleChange}
                  placeholder="Como o cliente conheceu a empresa?"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="address">Endereço</Label>
              <Input
                id="address"
                name="address"
                value={formData.address || ''}
                onChange={handleChange}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="city">Cidade</Label>
                <Input
                  id="city"
                  name="city"
                  value={formData.city || ''}
                  onChange={handleChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="state">Estado</Label>
                <Input
                  id="state"
                  name="state"
                  value={formData.state || ''}
                  onChange={handleChange}
                  maxLength={2}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="zip_code">CEP</Label>
                <Input
                  id="zip_code"
                  name="zip_code"
                  value={formData.zip_code || ''}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="notes">Observações</Label>
              <Textarea
                id="notes"
                name="notes"
                value={formData.notes || ''}
                onChange={handleChange}
                rows={4}
              />
            </div>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button type="button" variant="outline" onClick={() => navigate('/clients')}>
              Cancelar
            </Button>
            <Button type="submit" disabled={loading}>
              <Save className="mr-2 h-4 w-4" />
              {loading ? 'Salvando...' : 'Salvar'}
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
};

export default ClientForm;

